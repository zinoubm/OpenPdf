import os

from fastapi import UploadFile
import mimetypes
import pdfplumber
from textwrap3 import dedent
from unidecode import unidecode
import re

# import logging
from app.parser.parsers import *


# async def get_document_from_file(file: UploadFile, temp_file_path="/tmp/temp_file"):
#     mimetype = file.content_type
#     stream = await file.read()

#     with open(temp_file_path, "wb") as file:
#         file.write(stream)

#     try:
#         parsed_text = await extract_text_with_mimetype(temp_file_path, mimetype)

#     except Exception as e:
#         os.remove(temp_file_path)
#         raise Exception("Couldn't get document from file")

#     os.remove(temp_file_path)

#     return parsed_text


# async def get_document_from_file_stream(file_path):
#     try:
#         parsed_text = await extract_text_with_mimetype(file_path)

#     except Exception as e:
#         os.remove(file_path)
#         raise Exception("Couldn't get document from file")

#     os.remove(file_path)

#     return parsed_text

def get_document_from_file_stream(file_path, max_size = 2000):
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            # maybe should be removed
            if page_text == '':
                continue

            paragraphs = dedent(page_text)
            ascii_paragraphs = re.findall(r"[^.?!]+[(\.)?!]", unidecode(paragraphs))

            chunck = ""
            for sentence in ascii_paragraphs:
                if len(chunck) + len(sentence) < max_size:
                    chunck += sentence
                else:
                    yield chunck.strip()
                    chunck = ""

            if chunck.strip() is not None:
                yield chunck.strip()


# all parsers have to return generators from now on
# async def extract_text_with_mimetype(file_path, mimetype=None):
#     # logging.INFO(f"extracting text from file {file_path} and mimetype {mimetype}")
#     if mimetype is None:
#         mimetype, _ = mimetypes.guess_type(file_path)
#         # logging.INFO(f"File Mimetype Is: {mimetype}")
#     if mimetype is None:
#         raise Exception("Unsupported file type")

#     if mimetype == "application/pdf":
#         parsed_text = PdfParser.parse(file_path)

#     elif mimetype == "text/plain":
#         parsed_text = TxtParser.parse(file_path)

#     elif (
#         mimetype
#         == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#     ):
#         parsed_text = DocxParser.parse(file_path)

#     return parsed_text
