from numpy import dtype, int32, ndarray, unicode_
import pytest
from batala.components.ndarray_component_manager import NdarrayComponent, NdarrayComponentManager
from batala.engine.entity import Entity

test_entity = Entity(0, 0)
test_dtype = dtype([("int", int32), ("str", unicode_, 16)])


class TestComponent(NdarrayComponent):
    _dtype = test_dtype


class TestComponentManager(NdarrayComponentManager):
    _component_type = TestComponent


def test_init():
    component = TestComponent()
    assert component is not None
    assert isinstance(component, TestComponent)
    component_manager = TestComponentManager()
    assert component_manager is not None
    assert isinstance(component_manager, TestComponentManager)


def test_property():
    component = TestComponent()
    assert isinstance(component.data, ndarray)
    assert isinstance(component.dtype, dtype)
    assert component.dtype == test_dtype


def test_getitem():
    component = TestComponent((1, "test"))
    assert component["int"] == 1
    assert component["str"] == "test"
    with pytest.raises(ValueError):
        bad_item = component["bad"]


def test_setitem():
    component = TestComponent()
    component["int"] = 2
    component["str"] = "new"
    assert component["int"] == 2
    assert component["str"] == "new"


def test_register_component():
    component_manager = TestComponentManager()
    component_manager.register_component(test_entity, (0, "test"))
    assert component_manager.count == 1


def test_get_component():
    component_manager = TestComponentManager()
    component_manager.register_component(test_entity, (0, "test"))
    component = component_manager.get_component(test_entity)
    assert component is not None
    assert isinstance(component, TestComponent)
    assert component["int"] == 0
    assert component["str"] == "test"


def test_update_component():
    component_manager = TestComponentManager()
    component_manager.register_component(test_entity, (0, "test"))
    component_manager.update_component(test_entity, "int", 1)
    component_manager.update_component(test_entity, "str", "new")
    component = component_manager.get_component(test_entity)
    assert component is not None
    assert isinstance(component, TestComponent)
    assert component["int"] == 1
    assert component["str"] == "new"


def test_assign_component():
    component_manager = TestComponentManager()
    component_manager.register_component(test_entity, (0, "test"))
    new_component = TestComponent((1, "new"))
    component_manager.assign_component(test_entity, new_component)
    component = component_manager.get_component(test_entity)
    assert component["int"] == 1
    assert component["str"] == "new"


def test_destroy():
    component_manager = TestComponentManager()
    component_manager.register_component(test_entity)
    assert component_manager.count == 1
    component_manager.destroy(test_entity)
    assert component_manager.count == 0
    component = component_manager.get_component(test_entity)
    assert component is None


def test_iter():
    component_manager = TestComponentManager()
    for i in range(10):
        entity = Entity(i, 0)
        component_manager.register_component(entity, (i, str(i)))
    print(f"Count: {component_manager.count}")
    for component in component_manager:
        print(component)
        component_str = str(component["str"])
        assert str(component["int"]) == component_str
