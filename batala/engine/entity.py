from dataclasses import dataclass
from numpy import bitwise_and, bitwise_or, left_shift, right_shift
from batala.engine import GENERATION_MASK, INDEX_BITS, INDEX_MASK, Generation, Id, Index


@dataclass
class Entity():
    """An Entity is a simple dataclass that wraps an Id and exposes some
    utility methods. Id, Index, and Generation are typealiases defined in
    batala.engine.__init__.py
    """
    _id: Id

    def __init__(self, index: Index = 0, generation: Generation = 0, id: Id = None):
        """Initialize an Entity.

        Args:
            index (Index, optional): Index component of Id. Defaults to 0.
            generation (Generation, optional): Generation component of Id. Defaults to 0.
            id (Id, optional): Set Id to this value instead of generating. Defaults to None.
        """
        if id is not None:
            self._id = id
        else:
            self._id = self.generate_id(index, generation)

    @property
    def id(self) -> Id:
        """Get Id of the Entity.

        Returns:
            Id: the entity Id value (typealias Id defined in batala.engine.__init__.py)
        """
        return self._id

    @property
    def index(self) -> Index:
        """Get Index of the Entity from its Id.

        Returns:
            Index: the Index value of the entity Id (typealias Index defined in batala.engine.__init__.py)
        """
        return self.get_index(self._id)

    @property
    def generation(self) -> Generation:
        """Get Generation of the Entity from its Id.

        Returns:
            Generation: the Generation value of the entity Id (typealias Generation defined in batala.engine.__init__.py)
        """
        return self.get_generation(self._id)

    @staticmethod
    def generate_id(index: Index = 0, generation: Generation = 0) -> Id:
        """Get an Id from an Index value and a Generation value.

        First INDEX_BITS bits is the Index value, last GENERATION_BITS bits is
        Generation value.

        Args:
            index (Index, optional): Index value of the Id. Defaults to 0.
            generation (Generation, optional): Generation value of the Id. Defaults to 0.

        Returns:
            Id: the combined Id value (typealias Id defined in batala.engine.__init__.py)
        """
        return bitwise_or(index, left_shift(generation, INDEX_BITS))

    @staticmethod
    def get_index(id: Id) -> Index:
        """Get an Index from an Id
        First INDEX_BITS bits is the Index value, so bitwise_and with a mask
        gives us the value.

        Args:
            id (Id): the Id to query

        Returns:
            Index: the Index value of the Id
        """
        return bitwise_and(id, INDEX_MASK)

    @staticmethod
    def get_generation(id: Id) -> Generation:
        """Get a Generation from an Id
        Last GENERATION_BITS bits is the generation value, so right_shift then
        bitwise_and with mask gives us the value.

        Args:
            id (Id): the Id to query

        Returns:
            Generation: the Generation value of the Id
        """
        return bitwise_and(right_shift(id, INDEX_BITS), GENERATION_MASK)

    def __hash__(self) -> int:
        """Return hash (just the _id attribute)

        Returns:
            int: _description_
        """
        return self._id

    def __eq__(self, __value: object) -> bool:
        """Equals operator.

        Checks if __value is Entity, then compares _id values.

        Args:
            __value (object): object to compare, if not Entity will always be False

        Returns:
            bool: True if __value is Entity and _id values are equal
        """
        return isinstance(__value, Entity) and __value._id == self._id
