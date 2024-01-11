from app.parser.interface import ParserInterface
import docx


class DocxParser(ParserInterface):
    """
    A parser that extracts text from Microsoft Word documents.

    Methods:
        parse(file_path: str) -> str:
            Reads the given DOCX file and returns the concatenated text from all its paragraphs.
    """

    def parse(file_path) -> str:
        """
        Args:
            file_path (str): The path to the DOCX file to parse.

        Returns:
            str: The concatenated text from all paragraphs in the file.
        """
        document = docx.Document(file_path)
        return " ".join([paragraph.text for paragraph in document.paragraphs])
