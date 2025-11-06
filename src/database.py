from abc import abstractmethod

from typing_extensions import Protocol


class DatabaseInterface(Protocol):
    @abstractmethod
    def __init__(self, name: str):
        pass
