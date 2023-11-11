from numpy import array, dtype, ndarray, zeros
import pytest
from batala.components.ndarray_component_manager import NdarrayComponent
from batala.engine import Generation, Index
from batala.engine.entity import Entity
from batala.examples.classes.component_examples import (
    TestNdarrayComponentManager,
    test_dtype,
)


test_entity = Entity(Index(0), Generation(0))
test_data = array((1, "test"), dtype=test_dtype)


def test_init():
    component = NdarrayComponent(zeros(1, dtype=test_dtype))
    assert component is not None
    assert isinstance(component, NdarrayComponent)
    component_manager = TestNdarrayComponentManager()
    assert component_manager is not None
    assert isinstance(component_manager, TestNdarrayComponentManager)


def test_property():
    component = NdarrayComponent(zeros(1, dtype=test_dtype))
    assert isinstance(component.data, ndarray)
    assert isinstance(component.dtype, dtype)
    assert component.dtype == test_dtype


def test_getitem():
    component = NdarrayComponent(array((1, "test"), dtype=test_dtype))
    assert component["int"] == 1
    assert component["str"] == "test"
    with pytest.raises(ValueError):
        bad_item = component["bad"]


def test_setitem():
    component = NdarrayComponent(zeros(1, dtype=test_dtype))
    component["int"] = 2
    component["str"] = "new"
    assert component["int"] == 2
    assert component["str"] == "new"


def test_register_component():
    component_manager = TestNdarrayComponentManager()
    component_manager.register_component(test_entity)
    assert component_manager.count == 1


def test_get_component():
    component_manager = TestNdarrayComponentManager()
    component_manager.register_component(test_entity, test_data)
    component = component_manager.get_component(test_entity)
    assert component is not None
    assert isinstance(component, NdarrayComponent)
    assert component["int"] == 1
    assert component["str"] == "test"


def test_update_component():
    component_manager = TestNdarrayComponentManager()
    component_manager.register_component(test_entity, test_data)
    component_manager.update_component(test_entity, "int", 2)
    component_manager.update_component(test_entity, "str", "new")
    component = component_manager.get_component(test_entity)
    assert component is not None
    assert isinstance(component, NdarrayComponent)
    assert component["int"] == 2
    assert component["str"] == "new"


def test_assign_component():
    component_manager = TestNdarrayComponentManager()
    component_manager.register_component(test_entity)
    new_component = NdarrayComponent(test_data)
    component_manager.assign_component(test_entity, new_component)
    component = component_manager.get_component(test_entity)
    assert component is not None
    assert component["int"] == 1
    assert component["str"] == "test"


def test_destroy():
    component_manager = TestNdarrayComponentManager()
    component_manager.register_component(test_entity)
    assert component_manager.count == 1
    component_manager.destroy(test_entity)
    assert component_manager.count == 0
    component = component_manager.get_component(test_entity)
    assert component is None


def test_iter():
    component_manager = TestNdarrayComponentManager()
    for i in range(10):
        entity = Entity(Index(i), Generation(0))
        component_manager.register_component(entity, test_data)
    for component in component_manager:
        component_str = str(component["str"])
        assert component_str == "test"
