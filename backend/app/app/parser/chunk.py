from textwrap3 import dedent
from unidecode import unidecode
import re


def chunk_text(text, max_size=4000):
    paragraphs = dedent(text)
    ascii_paragraphs = re.findall(r"[^.?!]+[(\.)?!]", unidecode(paragraphs))

    chuncks = []
    chunck = ""
    for sentence in ascii_paragraphs:
        if len(chunck) + len(sentence) < max_size:
            chunck += sentence
        else:
            chuncks.append(chunck.strip())
            chunck = ""

    return chuncks
