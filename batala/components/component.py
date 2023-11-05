from abc import ABC, abstractmethod
from typing import Any


class Component(ABC):
    @abstractmethod
    def __getitem__(self, index: str):
        raise NotImplemented

    @abstractmethod
    def __setitem__(self, index: str, value: Any):
        raise NotImplemented
