import os

from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import StreamingResponse
from typing import Any, List
import mimetypes
from sqlalchemy.orm import Session

from app.openai.base import openai_manager
from app.openai.core import ask, ask_stream, suggest_questions
from app.vectorstore.qdrant import qdrant_manager
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core.constants import FEATURES_ENUM
from app.stripe.limiter import get_user_plan, get_user_limits

from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import FileTarget, ValueTarget
from streaming_form_data.validators import MaxSizeValidator

from app.aws.batch import aws_batch_manager

import boto3
from botocore.exceptions import ClientError

from .exeptions import MaxBodySizeValidator

router = APIRouter()

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
        filepath = os.path.join("/tmp", os.path.basename(filename))
        file_ = FileTarget(filepath, validator=MaxSizeValidator(MAX_FILE_SIZE))
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


        session = boto3.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )

        s3 = session.client("s3")

        bucket_name = os.getenv("AWS_BUCKET_NAME")

        object_key = (
            "documents"
            + "/"
            + "doc"
            + "-"
            + str(document.id)
            + ".pdf"
        )

        # Upload the file to S3
        s3.upload_file(
            filepath,
            bucket_name,
            object_key,
            ExtraArgs={"ContentType": "application/pdf"},
        )
        
        if settings.ENVIRONMENT == 'prod':
            response = aws_batch_manager.run({
                "user_id":str(current_user.id),
                "document_id":str(document.id)
            })

            print(response)
        
    except Exception as e:
        # remove later
        print(e)
        crud.document.remove(db=db, id=document.id)
        # delete s3 object in case of failure

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
) -> Any:
    """
    Retrieve documents.
    """
    if crud.user.is_superuser(current_user):
        documents = crud.document.get_multi(db, skip=skip, limit=limit)
    else:
        documents = crud.document.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )

    return documents


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
        session = boto3.Session(
            aws_access_key_id=settings.ACCESS_KEY_ID,
            aws_secret_access_key=settings.SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        s3 = session.client("s3")

        object_key = (
            "documents"
            + "/"
            + "doc"
            + "-"
            + str(document.id)
            + ".pdf"
        )

        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": os.getenv("AWS_BUCKET_NAME"),
                "Key": object_key,
            },
            ExpiresIn=10000,
        )

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
        limit=5,
    )

    context = "\n\n\n".join([point.payload["chunk"] for point in points])

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
        limit=5,
    )

    context = "\n\n\n".join([point.payload["chunk"] for point in points])

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
) -> Any:
    """
    Delete an document.
    """
    document = crud.document.get(db=db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not crud.user.is_superuser(current_user) and (
        document.user_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    try:
        qdrant_manager.delete_points(user_id=current_user.id, document_id=id)
        session = boto3.Session(
            aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )

        bucket_name = os.getenv("AWS_BUCKET_NAME")
        s3 = session.client("s3")

        object_key = (
            "documents"
            + "/"
            + "doc"
            + "-"
            + str(document.id)
            + ".pdf"
        )

        s3.delete_object(Bucket=bucket_name, Key=object_key)

    except Exception as e:
        raise HTTPException(
            status_code=502, detail="Something Went Wrong With The Vector Store!"
        )

    document = crud.document.remove(db=db, id=id)
    return document
