from abc import ABC, abstractmethod
from typing import Any


class Component(ABC):
    """Abstract base class for Components.
    All that is required is that a derived class can offer component
    values with the indexing [] operator. This means a component can
    be as simple as a dict wrapper, or a custom class
    """

    @abstractmethod
    def __getitem__(self, index: str):
        """Get a value in the component given the field name.

        Args:
            index (str): the field name of the requested value
        """
        raise NotImplemented

    @abstractmethod
    def __setitem__(self, index: str, value: Any):
        """Set a value in the component given the field name.

        Args:
            index (str): the field name of the requested value
        """
        raise NotImplemented
