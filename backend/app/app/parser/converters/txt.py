from app.parser.interface import ParserInterface


class TxtParser(ParserInterface):
    """
    A parser that reads text from plain text files.

    Methods:
        parse(file_path: str) -> str:
            Reads the given text file and returns its contents as a string.
    """

    def parse(file_path) -> str:
        """
        Args:
            file_path (str): The path to the text file to read.

        Returns:
            str: The contents of the text file as a string.
        """
        with open(file_path, "r") as file:
            txt = file.read()

        return txt
