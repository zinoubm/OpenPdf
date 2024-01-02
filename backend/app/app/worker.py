import os
import argparse

from app.core.config import settings
from uuid import uuid4
from app.openai.base import openai_manager
from app.vectorstore.qdrant import qdrant_manager
from app.parser.parser import get_document_from_file_stream

def parse_arg():
    """
    This function parses command line arguments to this script
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--user_id", type=int, default=1)
    parser.add_argument("--document_id", type=int, default=2)

    params = vars(parser.parse_args())

    return params

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
    # download s3 object
    
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
        
    return f"processing document {document_id}, with path {document_path} for user {user_id}"

if __name__ == "__main__":
    params = parse_arg()
    print(f"local batch container is working with {params}")
