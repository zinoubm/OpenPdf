import os

from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import StreamingResponse
from typing import List
import mimetypes
from sqlalchemy.orm import Session
from app.schemas.document import UpsertResponse

from app.openai.base import openai_manager
from app.openai.core import ask, ask_stream, suggest_questions
from app.vectorstore.qdrant import qdrant_manager
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core.constants import FEATURES_ENUM
from app.stripe.limiter import get_user_plan, get_user_limits

from app.parser.parser import process_document
from app.parser.parser import get_number_of_pages

from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import FileTarget, ValueTarget
from streaming_form_data.validators import MaxSizeValidator

from app.aws.batch import aws_batch_manager
from app.aws.s3 import aws_s3_manager

# import boto3
from botocore.exceptions import ClientError

from .exeptions import MaxBodySizeValidator

router = APIRouter()

# actually remove this and use documents less than 30 pages in development
# used for local dev
@router.post(
    "/upsert",
)
async def upsert_file(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if not file:
        print("There was a problem with file Upload")
        raise HTTPException(status_code=500, detail="No File Recieved")

    # Until openpdf supports more document formats
    if file.content_type != "application/pdf":
        print("OpenPdf only supports PDFs")
        raise HTTPException(
            status_code=415, detail="Openpdf Does Not Support Other Formats Yet!"
        )
    
    filename = file.filename
    temp_file_path="/tmp/temp_file"
    stream = await file.read()
    with open(temp_file_path, "wb") as file:
        file.write(stream)

    document_in = schemas.DocumentCreate(title=filename)
    document = crud.document.create_with_user(
        db=db, obj_in=document_in, user_id=current_user.id
    )
        
    aws_s3_manager.upload_s3_object(file_path=temp_file_path, document_id=document.id)

    process_document(user_id=current_user.id, document_id=document.id, document_path=temp_file_path)

    # set processed true
    updated_document_in = schemas.DocumentUpdate(is_processed=True)
    crud.document.update(db=db, db_obj=document, obj_in=updated_document_in)

    return {"document_id": document.id, "document_title": filename}


@router.post("/upsert-stream")
async def upsert_stream(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    # limiter
    user_plan, plan_status = get_user_plan(db=db, user_id=current_user.id)
    if plan_status != "ACTIVE":
        raise HTTPException(
            status_code=402,
            detail=f"Your plan ({user_plan}) Is non active!",
        )

    user_limits = get_user_limits(user_plan)
    usage = crud.user.get_usage(db=db, user_id=current_user.id)

    if usage[FEATURES_ENUM.UPLOADS] + 1 > user_limits[FEATURES_ENUM.UPLOADS]:
        raise HTTPException(
            status_code=402,
            detail=f"Max {FEATURES_ENUM.UPLOADS} limit exeeded for the {user_plan} plan!",
        )

    crud.user.increment_usage(
        db=db, user_id=current_user.id, feature=FEATURES_ENUM.UPLOADS
    )

    # upload
    MAX_REQUEST_BODY_SIZE = settings.MAX_REQUEST_BODY_SIZE
    MAX_FILE_SIZE = settings.MAX_FILE_SIZE

    body_validator = MaxBodySizeValidator(MAX_REQUEST_BODY_SIZE)
    filename = request.headers.get("Filename")

    # document = crud.document.get(db=db, title=filename)

    # if document and document.user_id == current_user.id and document.title == filename:
    #     raise HTTPException(status_code=400, detail="document already exists")

    if not filename:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Filename header is missing",
        )
    
    mimetype, _ = mimetypes.guess_type(filename)
    if mimetype != "application/pdf":
        raise HTTPException(
            status_code=415, detail="OpenPdfAI Does Not Support Other Formats Yet!"
        )
    
    try:
        temp_file_path = os.path.join("/tmp", os.path.basename(filename))
        file_ = FileTarget(temp_file_path, validator=MaxSizeValidator(MAX_FILE_SIZE))
        data = ValueTarget()
        parser = StreamingFormDataParser(headers=request.headers)
        parser.register("file", file_)
        parser.register("data", data)

        async for chunk in request.stream():
            body_validator(chunk)
            parser.data_received(chunk)

        document_in = schemas.DocumentCreate(title=file_.multipart_filename)
        document = crud.document.create_with_user(
            db=db, obj_in=document_in, user_id=current_user.id
        )

        aws_s3_manager.upload_s3_object(file_path=temp_file_path, document_id=document.id)

        pages_number = get_number_of_pages(temp_file_path)
        
        if pages_number <= 30:
            process_document(user_id=current_user.id, document_id=document.id, document_path=temp_file_path)

            # set processed true
            updated_document_in = schemas.DocumentUpdate(is_processed=True)
            crud.document.update(db=db, db_obj=document, obj_in=updated_document_in)

        elif settings.ENVIRONMENT == 'prod':
            response = aws_batch_manager.run({
                "user_id":str(current_user.id),
                "document_id":str(document.id)
            })
        
    except Exception as e:
        crud.document.remove(db=db, id=document.id)
        aws_s3_manager.delete_s3_object(document_id=document.id)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error uploading the file",
        )
    
    return {"document_id": document.id, "document_title": file_.multipart_filename}
    
@router.get("/", response_model=List[schemas.Document])
def read_documents(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if crud.user.is_superuser(current_user):
        documents = crud.document.get_multi(db, skip=skip, limit=limit)
    else:
        documents = crud.document.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )

    return documents

@router.get("/status")
def get_document_status(
    document_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    document = crud.document.get(db=db, id=document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return {"status" : document.is_processed}

@router.put("/status")
def set_document_status(
    secret: str,
    document_id: int,
    db: Session = Depends(deps.get_db),
):
    if secret != settings.DOCUMENT_PORECESSOR_SECRETE_KEY:
        raise HTTPException(
            status_code=403, detail="You Don't have the premission requred!"
        )

    document = crud.document.get(db=db, id=document_id)
    document_in = schemas.DocumentUpdate(is_processed=True)
    crud.document.update(db=db, db_obj=document, obj_in=document_in)
    return document_id


@router.get("/document-url")
def document_url(
    document_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    document = crud.document.get(db=db, id=document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    try:
        url = aws_s3_manager.get_s3_object_presigned_url(document_id=document.id)

    except ClientError:
        print("couldn't get document url")
        raise

    return {"url": url}


@router.post("/query")
async def query(
    query: str,
    document_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> str:
    document = crud.document.get(db=db, id=document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    query_vector = openai_manager.get_embedding(query)

    points = qdrant_manager.search_point(
        query_vector=query_vector,
        user_id=current_user.id,
        document_id=document_id,
        limit=16,
    )

    # context = "\n\n\n".join([point.payload["chunk"] for point in points])
    context = "\n\n\n".join([f"page: {point.payload.get('page', 'not provided')}, text: {point.payload['chunk']}" for point in points])


    answer = ask(
        context,
        query,
        openai_manager,
    )

    return {"answer": answer, "context": context}


@router.post("/query-stream")
async def query_stream(
    query_document: schemas.QueryDocument,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> str:
    query = query_document.query
    messages = query_document.messages
    document_id = query_document.document_id

    messages_in = []
    for message in messages:
        messages_in.append(
            {
                "role": message.entity,
                "content": message.message,
            }
        )

    # limiter will be a function
    user_plan, plan_status = get_user_plan(db=db, user_id=current_user.id)
    if plan_status != "ACTIVE":
        raise HTTPException(
            status_code=402,
            detail=f"Your plan ({user_plan}) Is non active!",
        )

    user_limits = get_user_limits(user_plan)
    usage = crud.user.get_usage(db=db, user_id=current_user.id)

    if usage[FEATURES_ENUM.QUERIES] + 1 > user_limits[FEATURES_ENUM.QUERIES]:
        raise HTTPException(
            status_code=402,
            detail=f"Max {FEATURES_ENUM.UPLOADS} limit exeeded for the {user_plan} plan!",
        )

    crud.user.increment_usage(
        db=db, user_id=current_user.id, feature=FEATURES_ENUM.QUERIES
    )

    # Qurey
    document = crud.document.get(db=db, id=document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    query_vector = openai_manager.get_embedding(query)

    points = qdrant_manager.search_point(
        query_vector=query_vector,
        user_id=current_user.id,
        document_id=document_id,
        limit=16,
    )

    context = "\n\n\n".join([f"page: {point.payload.get('page', 'not provided')}, text: {point.payload['chunk']}" for point in points])


    return StreamingResponse(
        ask_stream(
            context,
            query,
            messages_in,
            openai_manager,
        ),
        media_type="text/event-stream",
    )

@router.get("/question-suggestions")
async def suggest_question(
    document_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> str:
    document = crud.document.get(db=db, id=document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    query_vector = openai_manager.get_embedding("give a summary about this document")

    points = qdrant_manager.search_point(
        query_vector=query_vector,
        user_id=current_user.id,
        document_id=document_id,
        limit=5,
    )

    context = "\n\n\n".join([point.payload["chunk"] for point in points])

    suggestions = suggest_questions(context, manager=openai_manager)

    try:
        suggestions_list = [suggestion.strip() for suggestion in suggestions.split('\n')]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Couldn't parse suggestions!"
        )

    return {"suggestions": suggestions_list}


@router.delete("/{id}", response_model=schemas.Document)
def delete_document(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    document = crud.document.get(db=db, id=id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not crud.user.is_superuser(current_user) and (
        document.user_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    try:
        qdrant_manager.delete_points(user_id=current_user.id, document_id=id)
        aws_s3_manager.delete_s3_object(document_id=document.id)

    except Exception as e:
        raise HTTPException(
            status_code=502, detail="Something Went Wrong With The Vector Store!"
        )

    document = crud.document.remove(db=db, id=id)
    return document
