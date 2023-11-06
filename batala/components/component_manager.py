from abc import ABC, abstractmethod
from typing import Any, Callable

from semver import Version
from batala.components.component import Component

from batala.engine.entity import Entity
from batala.engine.plugin import PluginAPI


class ComponentManagerAPI(PluginAPI, version=Version(0, 0, 0)):
    register_component: Callable[[Entity], bool]
    get_component: Callable[[Entity], Component | None]
    update_component: Callable[[Entity, str, Any], Component | None]
    destroy: Callable[[Entity], bool]


class ComponentManager(ABC):
    """Base class for component managers to subclass
    Gives basic iterator functionality over instances as well as
    registering/updating/assigning instances.
    """

    @abstractmethod
    def register_component(self, entity: Entity) -> bool:
        """Register a component with the component manager

        Args:
            entity (Entity): Entity that will own this component instance

        Returns:
            bool: True of registration succeeded, else False
        """
        raise NotImplementedError

    @abstractmethod
    def get_component(self, entity: Entity) -> Component | None:
        """Get a component for a given entity

        Args:
            entity (Entity): Entity that owns the requested component

        Returns:
            Component | None: The component owned by entity, or None if none
                              found for given entity
        """
        raise NotImplementedError

    @abstractmethod
    def update_component(
        self, entity: Entity, field: str, value: Any
    ) -> Component | None:
        """Update a component for a given entity

        Args:
            entity (Entity): Entity that owns the requested component
            field (str): Name of the component field to update
            value (Any): Value to update the field with, must correspond with field type

        Returns:
            Component | None: The updated component, or None if none found for given entity
        """
        raise NotImplementedError

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
        raise NotImplementedError
