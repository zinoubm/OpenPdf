import argparse
import httpx
from app.core.config import settings
from app.parser.parser import process_document
from app.aws.s3 import aws_s3_manager

def parse_arg():
    """
    This function parses command line arguments to this script
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--user_id", type=int, default=1)
    parser.add_argument("--document_id", type=int, default=2)

    params = vars(parser.parse_args())

    return params

if __name__ == "__main__":
    params = parse_arg()
    user_id, document_id = params["user_id"], params["document_id"]

    object_key = f"documents/doc-{document_id}.pdf"  
    document_path = aws_s3_manager.download_s3_object(object_key = object_key)

    process_document(user_id=user_id, document_id=document_id, document_path=document_path)
    
    # todo: test later In production
    url = 'https://api.openpdfai.com/api/v1/documents/status'
    params = {'secret': settings.DOCUMENT_PORECESSOR_SECRETE_KEY, 'document_id': document_id}

    headers = {'accept': 'application/json'}

    response = httpx.put(url, headers=headers, params=params)
    # print(response)

    print(f"Document: {document_id}, Uploaded succefully")
