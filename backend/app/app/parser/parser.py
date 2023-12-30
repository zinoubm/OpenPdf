# import os

# from fastapi import UploadFile
# import mimetypes
# import pdfplumber
from pdfminer.layout import LAParams, LTTextBox #, LTTextLineHorizontal
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

# from textwrap3 import dedent
# from unidecode import unidecode
# import re

# from app.parser.parsers import *

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