import os

from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import StreamingResponse

from starlette.requests import ClientDisconnect

from typing import Any, List
from uuid import uuid4
import logging
from sqlalchemy.orm import Session

from app.schemas.document import UpsertResponse
from app.parser.parser import get_document_from_file, get_document_from_file_stream
from app.parser.chunk import chunk_text

from app.openai.base import openai_manager
from app.openai.core import ask, ask_stream
from app.vectorstore.qdrant import qdrant_manager
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import FileTarget, ValueTarget
from streaming_form_data.validators import MaxSizeValidator
import streaming_form_data

import boto3
from botocore.exceptions import ClientError
import os

from .exeptions import MaxBodySizeException, MaxBodySizeValidator

router = APIRouter()


@router.post(
    "/upsert",
    response_model=UpsertResponse,
)
async def upsert_file(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if not file:
        logging.error("There was a problem with file Upload")
        raise HTTPException(status_code=500, detail="No File Recieved")

    # Until openpdf supports more document formats
    if file.content_type != "application/pdf":
        logging.error("OpenPdf only supports PDFs")
        raise HTTPException(
            status_code=415, detail="Openpdf Does Not Support Other Formats Yet!"
        )

    document_text = await get_document_from_file(file)
    chunks = chunk_text(document_text, max_size=2000)

    document_in = schemas.DocumentCreate(title=file.filename)
    document = crud.document.create_with_user(
        db=db, obj_in=document_in, user_id=current_user.id
    )

    ids = [uuid4().hex for chunk in chunks]
    payloads = [
        {
            "user_id": current_user.id,
            "document_id": document.id,
            "chunk": chunk,
        }
        for chunk in chunks
    ]
    embeddings = openai_manager.get_embeddings(chunks)

    try:
        res = qdrant_manager.upsert_points(ids, payloads, embeddings)
        logging.info(f"Vector Store Response: {res}")

    except Exception as e:
        logging.error(e)
        crud.document.remove(db=db, id=document.id)
        qdrant_manager.delete_points(user_id=current_user.id, document_id=document.id)
        raise HTTPException(
            status_code=502, detail="Something Went Wrong With The Vector Store!"
        )

    logging.info(f"Document Uploaded Succesfuly")

    return UpsertResponse(id=document.id)


# Upload large documents
@router.post("/upsert-stream")
async def upsert_stream(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
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

        session = boto3.Session(
            aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )

        s3 = session.client("s3")

        bucket_name = os.getenv("AWS_BUCKET_NAME")

        document_in = schemas.DocumentCreate(title=file_.multipart_filename)
        document = crud.document.create_with_user(
            db=db, obj_in=document_in, user_id=current_user.id
        )

        object_key = (
            "documents"
            + "/"
            + "doc"
            + "-"
            + str(document.id)
            + "-"
            + file_.multipart_filename
        )

        # Upload the file to S3
        s3.upload_file(
            filepath,
            bucket_name,
            object_key,
            ExtraArgs={"ContentType": "application/pdf"},
        )

        document_text = await get_document_from_file_stream(filepath)
        chunks = chunk_text(document_text, max_size=2000)

        ids = [uuid4().hex for chunk in chunks]
        payloads = [
            {
                "user_id": current_user.id,
                "document_id": document.id,
                "chunk": chunk,
            }
            for chunk in chunks
        ]
        embeddings = openai_manager.get_embeddings(chunks)

    except ClientDisconnect:
        print("Client Disconnected")

    except MaxBodySizeException as e:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Maximum request body size limit ({MAX_REQUEST_BODY_SIZE} bytes) exceeded ({e.body_len} bytes read)",
        )

    except streaming_form_data.validators.ValidationError:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Maximum file size limit ({MAX_FILE_SIZE} bytes) exceeded",
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error uploading the file",
        )

    if not file_.multipart_filename:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="File is missing"
        )

    try:
        res = qdrant_manager.upsert_points(ids, payloads, embeddings)

    except Exception as e:
        crud.document.remove(db=db, id=document.id)
        qdrant_manager.delete_points(user_id=current_user.id, document_id=document.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Couldn't upload embeddings to the Vectorstore",
        )

    # return {"message": f"Successfuly uploaded {filename}"}
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
            aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )
        s3 = session.client("s3")

        # object_key = "documents" + "/" + document.title
        object_key = (
            "documents" + "/" + "doc" + "-" + str(document.id) + "-" + document.title
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

    return StreamingResponse(
        ask_stream(
            context,
            query,
            openai_manager,
        ),
        media_type="text/event-stream",
    )


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
            "documents" + "/" + "doc" + "-" + str(document.id) + "-" + document.title
        )
        s3.delete_object(Bucket=bucket_name, Key=object_key)

    except Exception as e:
        raise HTTPException(
            status_code=502, detail="Something Went Wrong With The Vector Store!"
        )

    document = crud.document.remove(db=db, id=id)
    return document
