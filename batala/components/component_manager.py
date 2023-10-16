from abc import ABC, abstractmethod
from typing import Any
from batala.components.component import Component

from batala.engine.entity import Entity


class ComponentManager(ABC):
    """Base class for component managers to subclass
    Gives basic iterator functionality over instances as well as
    registering/updating/assigning instances.
    """

    @abstractmethod
    def register_component(self, entity: Entity, data: Any = None):
        """Register a component with the component manager

        Args:
            entity (Entity): Entity that will own this component instance
            data (Any, optional): Data to initialize component with. Defaults to None.
        """
        raise NotImplemented

    @abstractmethod
    def get_component(self, entity: Entity) -> Component | None:
        """Get a component for a given entity

        Args:
            entity (Entity): Entity that owns the requested component

        Returns:
            Component | None: The component owned by entity, or None if none found for given entity
        """
        raise NotImplemented

    @abstractmethod
    def update_component(self, entity: Entity, field: str, value: Any) -> Component | None:
        """Update a component for a given entity

        Args:
            entity (Entity): Entity that owns the requested component
            field (str): Name of the component field to update
            value (Any): Value to update the field with, must correspond with field type

        Returns:
            Component | None: The updated component, or None if none found for given entity
        """
        raise NotImplemented

    @abstractmethod
    def assign_component(self, entity: Entity, instance: Component) -> bool:
        """Assigns component instance to existing entity component slot

        Args:
            entity (Entity): Entity that owns the component
            instance (ndarray): Instance data to assign

        Returns:
            bool: True if entity is registered, False if not
        """
        raise NotImplemented

    @abstractmethod
    def destroy(self, entity: Entity) -> bool:
        """Destroy a component owned by the given entity

        Args:
            entity (Entity): Entity that owns the component

        Returns:
            bool: True if entity is registered, False if not
        """
        raise NotImplementedError

    @abstractmethod
    def __iter__(self):
        raise NotImplemented
