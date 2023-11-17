from numpy import array
from batala.components.ndarray_component_manager import NdarrayComponent
from batala.components.transform2d_component_manager import (
    Transform2D,
    Transform2DComponentManager,
)
from batala.engine import Generation, Index
from batala.engine.entity import Entity


test_entity = Entity(Index(0), Generation(0))
test_data = array((250, 250, 0, 0, 10, 10), dtype=Transform2D)


def test_init():
    component_manager = Transform2DComponentManager()
    assert component_manager is not None
    assert isinstance(component_manager, Transform2DComponentManager)


def test_register_component():
    component_manager = Transform2DComponentManager()
    component_manager.register_component(test_entity)
    assert component_manager.count == 1


def test_get_component():
    component_manager = Transform2DComponentManager()
    component_manager.register_component(test_entity, test_data)
    component = component_manager.get_component(test_entity)
    assert component is not None
    assert isinstance(component, NdarrayComponent)
    assert component["x"] == test_data["x"]
    assert component["y"] == test_data["y"]


def test_update_component():
    component_manager = Transform2DComponentManager()
    component_manager.register_component(test_entity, test_data)
    component_manager.update_component(test_entity, "x", 0)
    component_manager.update_component(test_entity, "y", 0)
    component = component_manager.get_component(test_entity)
    assert component is not None
    assert isinstance(component, NdarrayComponent)
    assert component["x"] == 0
    assert component["y"] == 0


def test_assign_component():
    component_manager = Transform2DComponentManager()
    component_manager.register_component(test_entity)
    new_component = NdarrayComponent(test_data)
    component_manager.assign_component(test_entity, new_component)
    component = component_manager.get_component(test_entity)
    assert component is not None
    assert component["x"] == test_data["x"]
    assert component["y"] == test_data["y"]


def test_destroy():
    component_manager = Transform2DComponentManager()
    component_manager.register_component(test_entity)
    assert component_manager.count == 1
    component_manager.destroy(test_entity)
    assert component_manager.count == 0
    component = component_manager.get_component(test_entity)
    assert component is None


def test_iter():
    component_manager = Transform2DComponentManager()
    for i in range(10):
        entity = Entity(Index(i), Generation(0))
        component_manager.register_component(entity, test_data)
    for component in component_manager:
        assert component["x"] == 250
        assert component["y"] == 250
