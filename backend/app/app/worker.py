from celery import Celery
from app.core.config import settings
import time

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

# celery.conf.task_routes = {"app.worker.process_document": "main-queue"}

# @celery.task(acks_late=True)
# async def test_celery(word: str) -> str:
#     return f"test task return {word}"


@celery.task(acks_late=True)
def process_document(document_path: str) -> str:
    time.sleep(30)
    return f"processing document {document_path}"
