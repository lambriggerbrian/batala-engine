from collections import deque
from batala.engine import MAX_ENTITIES
from batala.engine.entity import Entity
from numpy import ndarray, uint32, zeros


class EntityManager():
    _entities: ndarray
    _free_indices: deque[uint32]
    count: int

    def __init__(self):
        self._entities = zeros(MAX_ENTITIES, dtype=Entity)
        self._free_indices = deque()

    def create(self):
        pass

    def is_alive(self, entity: Entity) -> bool:
        pass

    def destroy(self, entity: Entity):
        pass
