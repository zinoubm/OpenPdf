from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import resolve1

from app.openai.base import openai_manager
from app.vectorstore.qdrant import qdrant_manager
from uuid import uuid4
import os


def get_document_from_file_stream(file_path):
    fp = open(file_path, 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp, check_extractable=False)

    for page_num, page in enumerate(pages, start=1):
        interpreter.process_page(page)
        layout = device.get_result()

        for paragraph in layout:
            if isinstance(paragraph, LTTextBox):
                b0, b1, b2, b3, text = paragraph.bbox[0], paragraph.bbox[1], paragraph.bbox[2], paragraph.bbox[3], paragraph.get_text()

                yield {
                        "page":page_num,
                        "text":text.strip(),
                        "version":1,
                        "b0":b0,
                        "b1":b1,
                        "b2":b2,
                        "b3":b3
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
            parser = PDFParser(f)
            doc = PDFDocument(parser)
            parser.set_document(doc)
            pages = resolve1(doc.catalog['Pages'])
            pages_count = pages.get('Count', 0)
            
        return pages_count
    except Exception as e:
        print(e)
        return None
