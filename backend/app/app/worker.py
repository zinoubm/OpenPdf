from celery import Celery
from app.core.config import settings
from app import schemas
import time

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

@celery.task(acks_late=True)
def process_document(user_id: int, document_id: int, document_path: str) -> str:
    time.sleep(10)
    return f"processing document {document_id}, with path {document_path} for user {user_id}"
