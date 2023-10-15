from abc import ABC, abstractmethod
from typing import Any, TypeVar

from numpy import ndarray


ComponentLike = TypeVar("ComponentLike", tuple, ndarray)


class Component(ABC):
    @abstractmethod
    def __getitem__(self, index: int | str):
        raise NotImplemented

    @abstractmethod
    def __setitem__(self, index: int | str, value: Any):
        raise NotImplemented
