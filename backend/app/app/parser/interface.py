from abc import ABC, abstractmethod


class ParserInterface(ABC):
    @abstractmethod
    def parse(file_path) -> str:
        pass
