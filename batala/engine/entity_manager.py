from collections import deque

import numpy
from batala.engine import (
    MAX_ENTITIES,
    MAX_GENERATION_VALUE,
    MINIMUM_FREE_INDICES,
    Generation,
    Id,
    Index,
)
from batala.engine.entity import Entity
from numpy import ndarray, full


class EntityManager:
    """An EntityManager creates and monitors Entities by maintaining an array
    of Generation values.
    """

    _entities: ndarray
    _free_indices: deque[Index]
    _back: int = 0
    _count: int = 0

    def __init__(self):
        """Initializes an empty EntityManager with MAX_ENTITIES capacity.

        MAX_ENTITIES is defined in batala.engine.__init__.py
        """
        self._entities = full(MAX_ENTITIES, MAX_GENERATION_VALUE, dtype=Generation)
        self._free_indices = deque()

    def create(self) -> Entity:
        """Create an Entity.

        The entity Id will have an Index and Generation value according to the
        EntityManager state.

        Returns:
            Entity: the created entity
        """
        index = Index(self._back)
        if len(self._free_indices) > MINIMUM_FREE_INDICES:
            index = self._free_indices.popleft()
        assert index < MAX_ENTITIES
        # If value is MAX_GENERATION_VALUE, this index has never been used
        if self._entities[index] == MAX_GENERATION_VALUE:
            self._entities[index] = 0
        generation = self._entities[index]
        assert generation < MAX_GENERATION_VALUE
        self._back += 1
        self._count += 1
        return Entity(index, generation)

    def __getitem__(self, entity: Entity | Id) -> Entity | None:
        if isinstance(entity, numpy.unsignedinteger):
            entity = Entity(id=entity)
        if not isinstance(entity, Entity) or not self.is_alive(entity):
            return None
        return entity

    def is_alive(self, entity: Entity) -> bool:
        """Check if an Entity is alive.

        An Entity is alive if its Generation value is equal to the Generation
        value at the Index of the EntityManager.

        Args:
            entity (Entity): the Entity to query with

        Returns:
            bool: True if the Entity is alive, else False
        """
        return self._entities[entity.index] == entity.generation

    def destroy(self, entity: Entity) -> bool:
        """Destroy an Entity.

        Increment the Generation value at Entity's Index, add the Index to the
        _free_indices queue for recycling, and decrement _count.

        Args:
            entity (Entity): the Entity to destroy

        Returns:
            bool: True if entity is alive and successfully destroyed, else False
        """
        # Make sure we don't have a stale Entity
        if not self.is_alive(entity):
            return False
        index = entity.index
        self._entities[index] += 1
        self._free_indices.append(index)
        self._count -= 1
        return True

    @property
    def count(self) -> int:
        """Get the count of living Entities.

        Returns:
            int: the number of living Entities
        """
        return self._count
