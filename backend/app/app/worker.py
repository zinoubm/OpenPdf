import os

from celery import Celery
from app.core.config import settings
from uuid import uuid4
from app.openai.base import openai_manager
from app.vectorstore.qdrant import qdrant_manager
from app.parser.parser import get_document_from_file_stream
import boto3

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

def upload_s3(document_path, document_id):
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
        + str(document_id)
        + ".pdf"
    )

    # Upload the file to S3
    s3.upload_file(
        document_path,
        bucket_name,
        object_key,
        ExtraArgs={"ContentType": "application/pdf"},
    )

def upload_batch(batch, user_id, document_id):
    ids = [uuid4().hex for batch_chunk in batch]
    payloads = [
        {
            "user_id": user_id,
            "document_id": document_id,
            "chunk": batch_chunk["text"],
            "page": batch_chunk["page"],
            "version": batch_chunk["version"]
        }
        for batch_chunk in batch
    ]
    current_batch_text = [chunck["text"] for chunck in batch]
    embeddings = openai_manager.get_embeddings(current_batch_text)

    res = qdrant_manager.upsert_points(ids, payloads, embeddings)


@celery.task(acks_late=True)
def process_document(user_id: int, document_id: int, document_path: str) -> str:

    chuncks = get_document_from_file_stream(document_path)
    batch_size = 256
    current_batch = []

    for chunk in chuncks:
        current_batch.append(chunk)

        if len(current_batch) == batch_size:
            upload_batch(batch=current_batch, user_id=user_id, document_id=document_id)
            current_batch = []

    if current_batch:
        upload_batch(batch=current_batch, user_id=user_id, document_id=document_id)
        
    os.remove(document_path)
    return f"processing document {document_id}, with path {document_path} for user {user_id}"
