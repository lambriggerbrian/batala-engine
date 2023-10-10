from collections import deque
from batala.engine import MAX_ENTITIES, MINIMUM_FREE_INDICES, Generation, Index
from batala.engine.entity import Entity
from numpy import ndarray, zeros


class EntityManager():
    _entities: ndarray
    _free_indices: deque[Index]
    _back: int = 0
    _count: int = 0

    def __init__(self):
        self._entities = zeros(MAX_ENTITIES, dtype=Generation)
        self._free_indices = deque()

    def create(self) -> Entity:
        index = Index(self._back)
        if len(self._free_indices) > MINIMUM_FREE_INDICES:
            index = Index(self._free_indices.popleft())
        assert index < MAX_ENTITIES
        generation = self._entities[index]
        self._back += 1
        self._count += 1
        return Entity(index, generation)

    def is_alive(self, entity: Entity) -> bool:
        return self._entities[entity.index] == entity.generation

    def destroy(self, entity: Entity):
        index = entity.index
        self.entities[index] += 1
        self._free_indices.append(index)
        self.count -= 1

    @property
    def count(self):
        return self._count
