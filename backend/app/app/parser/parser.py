import os

from fastapi import UploadFile
import mimetypes
from app.parser.parsers import *


async def get_document_from_file(file: UploadFile, temp_file_path="/tmp/temp_file"):
    mimetype = file.content_type
    stream = await file.read()

    with open(temp_file_path, "wb") as file:
        file.write(stream)

    try:
        parsed_text = await extract_text_with_mimetype(temp_file_path, mimetype)

    except Exception as e:
        os.remove(temp_file_path)
        raise Exception("Couldn't get document from file")

    os.remove(temp_file_path)

    return parsed_text


async def extract_text_with_mimetype(file_path, mimetype):
    if mimetype is None:
        mimetype, _ = mimetypes.guess_type(file_path)

    if mimetype is None:
        raise Exception("Unsupported file type")

    if mimetype == "application/pdf":
        parsed_text = PdfParser.parse(file_path)

    elif mimetype == "text/plain":
        parsed_text = TxtParser.parse(file_path)

    elif (
        mimetype
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        parsed_text = DocxParser.parse(file_path)

    return parsed_text
