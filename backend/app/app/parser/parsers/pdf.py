from app.parser.interface import ParserInterface
import pdfplumber


class PdfParser(ParserInterface):
    """
    A parser that extracts text from PDF documents.

    Methods:
        parse(file_path: str) -> str:
            Reads the given PDF file and returns the concatenated text from all its pages.
    """

    def parse(file_path) -> str:
        """
        Args:
            file_path (str): The path to the PDF file to parse.

        Returns:
            str: The concatenated text from all pages in the file.
        """
        pdf = pdfplumber.open(file_path)
        return " ".join([page.extract_text() for page in pdf.pages])
