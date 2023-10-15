from numpy import array, ndarray, dtype, nditer, zeros
from batala.components.component import Component, ComponentLike
from batala.components.component_manager import ComponentManager
from batala.engine import MAX_ENTITIES
from batala.engine.entity import Entity


class NdarrayComponent(Component):
    _data: ndarray
    _dtype: dtype

    def __init__(self, data: tuple | ndarray | None = None):
        if data is None:
            data = zeros([1], dtype=self._dtype)
        if isinstance(data, tuple):
            data = array(data, dtype=self._dtype)
        if data.dtype != self._dtype:
            raise TypeError(
                f"Expected data of type {self._dtype}, received: {data.dtype}")
        self._data = data

    @property
    def data(self):
        return self._data

    @property
    def dtype(self):
        return self._dtype

    def __getitem__(self, index: int | str):
        return self._data[index]

    def __setitem__(self, index: int | str, value: ComponentLike):
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
    _dtype: dtype
    _component_type: NdarrayComponent
    # A numpy array containing all instance data (to be declared by subclasses)
    instances: ndarray
    # A hashmap of entities to their component indexes (to be declared by subclasses)
    instance_map: dict[Entity, int] = {}
    index_map: dict[int, Entity] = {}
    # Number of instances registered
    count: int = 0

    def __init__(self) -> None:
        self._dtype = self._component_type._dtype
        self.instances = zeros([MAX_ENTITIES], dtype=self._dtype)

    def register_component(self, entity: Entity, data: ComponentLike | None = None):
        """Register a component with the component manager

        Args:
            entity (Entity): Entity that will own this component instance
            data (ndarray | None, optional): Data to initialize component with. Defaults to None.
        """
        index = self.count
        if isinstance(data, tuple):
            data = array(data, dtype=self._dtype)
        if data is None or data.dtype != self._dtype:
            data = zeros([1], dtype=self._dtype)
        self.instances[index] = data
        self.instance_map[entity] = index
        self.index_map[index] = entity
        self.count += 1

    def get_component(self, entity: Entity) -> NdarrayComponent | None:
        if not entity in self.instance_map:
            return None
        index = self.instance_map[entity]
        return self._component_type(self.instances[index])

    def update_component(self, entity: Entity, field: str | int, value: ComponentLike) -> NdarrayComponent | None:
        """Update a component for a given entity

        Args:
            entity (Entity): Entity that owns the requested component
            field (str): Name of the component field to update
            value (Any): Value to update the field with, must correspond with field type

        Returns:
            ndarray | None: The updated component, or None if none found for given entity
        """
        if not entity in self.instance_map:
            return None
        index = self.instance_map[entity]
        self.instances[index][field] = value
        return self._component_type(self.instances[index])

    def assign_component(self, entity: Entity, instance: NdarrayComponent) -> int | None:
        """Assigns component instance to existing entity component slot

        Args:
            entity (Entity): Entity that owns the component
            instance (ndarray): Instance data to assign

        Returns:
            int | None: the index of the assigned component or None if entity is not registered
        """
        if not entity in self.instance_map:
            return None
        index = self.instance_map[entity]
        self.instances[index] = instance.data
        return index

    def destroy(self, entity: Entity):
        """Destroy a component owned by the given entity

        Args:
            entity (Entity): Entity that owns the component
        """
        entity_index = self.instance_map.pop(entity, None)
        if entity_index is None:
            return
        last_index = self.count-1
        last_entity = self.index_map[last_index]
        last_instance = self.instances[last_index]
        self.instances[entity_index] = last_instance
        if self.count > 1:
            self.instance_map[last_entity] = entity_index
            self.index_map[entity_index] = last_entity
        self.count -= 1

    def __iter__(self):
        for i in range(self.count):
            yield self.instances[i]
