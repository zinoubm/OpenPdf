import os
from pypdf import PdfReader

from app.openai.base import openai_manager
from app.vectorstore.qdrant import qdrant_manager
from uuid import uuid4



def get_document_from_file_stream(file_path):
    reader = PdfReader(file_path)

    for page_num, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text == '':
            continue

        yield {
                "page":page_num,
                "text":page_text.strip(),
                "version":1
              }
        
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


def process_document(user_id: int, document_id: int, document_path: str) -> str:
    chuncks = get_document_from_file_stream(document_path)
    batch_size = 256
    current_batch = []

    for chunk in chuncks:
        print(f"Uploading batch for user {user_id}")
        current_batch.append(chunk)

        if len(current_batch) == batch_size:
            upload_batch(batch=current_batch, user_id=user_id, document_id=document_id)
            current_batch = []

    if current_batch:
        upload_batch(batch=current_batch, user_id=user_id, document_id=document_id)

    os.remove(document_path)
    return f"processing document {document_id}, with path {document_path} for user {user_id}"


def get_number_of_pages(file_path):
    try:
        with open(file_path, 'rb') as f:
            pdfReader = PdfReader(f)
            pages_count = len(pdfReader.pages)

        return pages_count
    except Exception as e:
        print(e)
        return None
