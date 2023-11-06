from typing import Any
from numpy import array, ndarray, dtype, zeros
from batala.components.component import Component
from batala.components.component_manager import ComponentManager
from batala.engine import MAX_ENTITIES
from batala.engine.entity import Entity


class NdarrayComponent(Component):
    _data: ndarray

    def __init__(self, data: ndarray):
        self._data = data

    @property
    def data(self):
        return self._data

    @property
    def dtype(self):
        return self._data.dtype

    def __getitem__(self, index: int | str):
        return self._data[index]

    def __setitem__(self, index: int | str, value: Any):
        self._data[index] = value

    def __repr__(self) -> str:
        return self._data.__repr__()

    def __str__(self) -> str:
        return self._data.__str__()


class NdarrayComponentManager(ComponentManager):
    """Base class for component managers to subclass
    Gives basic iterator functionality over instances as well as
    registering/updating/assigning instances.
    """

    component_type: dtype
    # A numpy array containing all instance data (to be declared by subclasses)
    instances: ndarray
    instance_map: dict[Entity, int] = {}
    index_map: dict[int, Entity] = {}
    # Number of instances registered
    count: int = 0

    def __init__(self, dtype: dtype):
        self.component_type = dtype
        self.instances = zeros([MAX_ENTITIES], dtype=self.component_type)

    def register_component(self, entity: Entity, data: ndarray | None = None) -> bool:
        """Register a component with the component manager

        Args:
            entity (Entity): Entity that will own this component instance
            data (ndarray | None, optional): Data to initialize component with. Defaults to None.
        """
        index = self.count
        if data is None:
            data = zeros(1, dtype=self.component_type)
        if data.dtype != self.component_type:
            return False
        self.instances[index] = data
        self.instance_map[entity] = index
        self.index_map[index] = entity
        self.count += 1
        return True

    def get_component(self, entity: Entity) -> NdarrayComponent | None:
        if entity not in self.instance_map:
            return None
        index = self.instance_map[entity]
        return NdarrayComponent(self.instances[index])

    def update_component(
        self, entity: Entity, field: str | int, value: Any
    ) -> NdarrayComponent | None:
        """Update a component for a given entity

        Args:
            entity (Entity): Entity that owns the requested component
            field (str): Name of the component field to update
            value (Any): Value to update the field with, must correspond with field type

        Returns:
            ndarray | None: The updated component, or None if none found for given entity
        """
        if entity not in self.instance_map:
            return None
        index = self.instance_map[entity]
        self.instances[index][field] = value
        return NdarrayComponent(self.instances[index])

    def assign_component(self, entity: Entity, instance: NdarrayComponent) -> bool:
        """Assigns component instance to existing entity component slot

        Args:
            entity (Entity): Entity that owns the component
            instance (ndarray): Instance data to assign

        Returns:
            bool: True if entity is registered, False if not
        """
        if entity not in self.instance_map:
            return False
        index = self.instance_map[entity]
        self.instances[index] = instance.data
        return True

    def destroy(self, entity: Entity) -> bool:
        """Destroy a component owned by the given entity

        Args:
            entity (Entity): Entity that owns the component

        Returns:
            bool: True if entity is registered, False if not
        """
        entity_index = self.instance_map.pop(entity, None)
        if entity_index is None:
            return False
        last_index = self.count - 1
        last_entity = self.index_map[last_index]
        last_instance = self.instances[last_index]
        self.instances[entity_index] = last_instance
        if self.count > 1:
            self.instance_map[last_entity] = entity_index
            self.index_map[entity_index] = last_entity
        self.count -= 1
        return True

    def __iter__(self):
        for i in range(self.count):
            yield self.instances[i]
