from numpy import dtype
import numpy
from batala.components.ndarray_component_manager import (
    NdarrayComponent,
    NdarrayComponentManagerAPI,
)
from batala.components.transform2d_component_manager import (
    Transform2D,
    Transform2DComponentManager,
)
from batala.engine.entity import Entity
from batala.engine.utils import Registry
from batala.systems.physics2d import Physics2DSystem


test_entity = Entity(0, 0)
one_second = 10**9
test_array = numpy.array((0, 0, 0, 0, -10, -10), dtype=Transform2D)


def test_init():
    system = Physics2DSystem()
    assert system is not None
    assert isinstance(system, Physics2DSystem)


def test_step():
    system = Physics2DSystem()
    component_manager = Transform2DComponentManager()
    component_manager.register_component(test_entity)
    component_manager.assign_component(test_entity, NdarrayComponent(test_array))
    api = NdarrayComponentManagerAPI(
        register_component=component_manager.register_component,
        get_component=component_manager.get_component,
        update_component=component_manager.update_component,
        assign_component=component_manager.assign_component,
        destroy=component_manager.destroy,
        iter=component_manager.__iter__,
    )
    system.apis = Registry(
        {"Transform2DPlugin": Registry({"NdarrayComponentManagerAPI": api})}
    )
    expected_value = 0
    expected_value_prime = 0
    for i in range(10):
        expected_value_prime = (i + 1) * -10
        expected_value += expected_value_prime
        system.step(one_second)
        component = component_manager.get_component(test_entity)
        assert component is not None
        assert component["x"] == expected_value
        assert component["y"] == expected_value
        assert component["x'"] == expected_value_prime
        assert component["y'"] == expected_value_prime
