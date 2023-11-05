from typing import Any
from numpy import dtype, int32, unicode_
from batala.components.component import Component
from batala.components.component_manager import ComponentManager
from batala.components.ndarray_component_manager import (
    NdarrayComponent,
    NdarrayComponentManager,
)
from batala.engine.entity import Entity


class TestComponent(Component):
    values: dict[str, int]

    def __init__(self) -> None:
        self.values = {"discrete_steps": 0, "continuous_time": 0}

    def __getitem__(self, index: str):
        return self.values[index]

    def __setitem__(self, index: str, value: int):
        self.values[index] = value


class TestComponentManager(ComponentManager):
    components: dict[Entity, TestComponent]

    def __init__(self) -> None:
        self.components = {}

    def register_component(self, entity: Entity):
        self.components[entity] = TestComponent()

    def get_component(self, entity: Entity) -> Component | None:
        return self.components.get(entity)

    def update_component(
        self, entity: Entity, field: str, value: Any
    ) -> Component | None:
        component = self.components.get(entity)
        if component:
            component[field] = value
        return component

    def destroy(self, entity: Entity) -> bool:
        if entity not in self.components:
            return False
        _ = self.components.pop(entity)
        return True

    def __iter__(self):
        return iter(self.components.values())


test_dtype = dtype([("int", int32), ("str", unicode_, 16)])


class TestNdarrayComponentManager(NdarrayComponentManager):
    _dtype = test_dtype

    def __init__(self):
        super().__init__(self._dtype)
