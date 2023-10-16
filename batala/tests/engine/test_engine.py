from typing import Any
from semver import Version
from batala.components.component import Component
from batala.components.component_manager import ComponentManager
from batala.engine import Id
from batala.engine.engine import Engine
from batala.engine.entity import Entity
from batala.engine.module import Module, ModuleType
from batala.systems.system import System


class TestComponent(Component):
    values: dict[str, int] = {"discrete_steps": 0, "continuous_time": 0}

    def __getitem__(self, index: str):
        return self.values[index]

    def __setitem__(self, index: str, value: int):
        self.values[index] = value


class TestComponentManager(Module, ComponentManager):
    _name = "TestComponentManager"
    _version = Version(1, 0, 0)
    _type = ModuleType.COMPONENT
    instances: dict[Entity, TestComponent] = {}

    def register_component(self, entity: Entity, data: TestComponent = None):
        if data is None:
            data = TestComponent()
        self.instances[entity] = data

    def get_component(self, entity: Entity) -> Component | None:
        return self.instances[entity]

    def update_component(self, entity: Entity, field: str, value: Any) -> Component | None:
        self.instances[entity][field] = value
        return self.instances[entity]

    def assign_component(self, entity: Entity, instance: Component) -> bool:
        if entity not in self.instances:
            return False
        self.instances[entity] = instance
        return True

    def destroy(self, entity: Entity):
        if entity not in self.instances:
            return False
        self.instances.pop(entity)

    def __iter__(self):
        for value in self.instances.values():
            yield value


class TestSystem(Module, System):
    _name = "TestSystem"
    _version = Version(1, 0, 0)
    _type = ModuleType.SYSTEM
    _dependencies = [Module.generate_moduleId(
        "TestComponentManager", Version(1, 0, 0))]

    def step(self, delta_time):
        for component in self._id_to_dependency[self._dependencies[0]]:
            component["discrete_steps"] += 1
            component["continuous_time"] += delta_time


def test_init():
    engine = Engine()
    assert engine is not None
    assert isinstance(engine, Engine)


def test_register_module():
    engine = Engine()
    test_component_manager = TestComponentManager()
    engine.register_module(test_component_manager)
    moduleId = test_component_manager.moduleId
    module = engine.modules[moduleId]
    assert module == test_component_manager


def test_create_entity():
    test_component_manager = TestComponentManager()
    engine = Engine([test_component_manager])
    moduleId = test_component_manager.moduleId
    entity = engine.create_entity([moduleId])
    component = engine.component_managers[moduleId].get_component(entity)
    assert component is not None
    assert component["discrete_steps"] == 0
    assert component["continuous_time"] == 0


def test_step():
    test_component_manager = TestComponentManager()
    test_system = TestSystem()
    engine = Engine([test_component_manager, test_system])
    moduleId = test_component_manager.moduleId
    entity = engine.create_entity([moduleId])
    for i in range(10):
        engine.step(60)
        component = test_component_manager.get_component(entity)
        assert component["discrete_steps"] == i+1
        assert component["continuous_time"] == (i+1)*60
        assert engine.frame_times[i] is not None
