from celery import Celery
from app.core.config import settings
from app import schemas
import time
import os

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

@celery.task(acks_late=True)
def process_document(user_id: int, document_id: int, document_path: str) -> str:
    files = os.listdir('/tmp')
    print("printing files in tmp")
    for file in files:
        print(file)

    time.sleep(5)
    os.remove(document_path)
    return f"processing document {document_id}, with path {document_path} for user {user_id}"
