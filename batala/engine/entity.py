from dataclasses import dataclass
from numpy import bitwise_and, bitwise_or, left_shift, right_shift
from batala.engine import GENERATION_MASK, INDEX_BITS, INDEX_MASK, Generation, Id, Index


@dataclass
class Entity():
    _id: Id

    def __init__(self, index: Index = 0, generation: Generation = 0, id: Id = None):
        if id is not None:
            self._id = id
        else:
            self._id = self.generate_id(index, generation)

    @property
    def id(self) -> Id:
        return self._id

    @property
    def index(self) -> Index:
        return self.get_index(self._id)

    @property
    def generation(self) -> Generation:
        return self.get_generation(self._id)

    def generate_id(self, index: Index = 0, generation: Generation = 0) -> Id:
        return bitwise_or(index, left_shift(generation, self._index))

    @staticmethod
    def get_index(id: Id) -> Index:
        return bitwise_and(id, INDEX_MASK)

    @staticmethod
    def get_generation(id: Id) -> Generation:
        return bitwise_and(right_shift(id, INDEX_BITS), GENERATION_MASK)

    def __hash__(self) -> int:
        return self._id
