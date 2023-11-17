from batala.components.ndarray_component_manager import NdarrayComponentManagerAPI
from batala.components.transform2d_component_manager import (
    Transform2DComponentManager,
)
from batala.engine.entity import Entity
from batala.engine.utils import Registry
from batala.systems.physics2d import ACCUMULATOR_THRESHOLD, Physics2DSystem


test_entity = Entity(0, 0)
half_step = ACCUMULATOR_THRESHOLD // 2


def test_init():
    system = Physics2DSystem()
    assert system is not None
    assert isinstance(system, Physics2DSystem)


def test_step():
    system = Physics2DSystem()
    component_manager = Transform2DComponentManager()
    component_manager.register_component(test_entity)
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
    expected_y = 0
    expected_y_prime = 0
    for i in range(10):
        steps = (i + 1) // 2
        expected_y_prime = steps
        expected_y += expected_y_prime
        system.step(half_step)
        component = component_manager.get_component(test_entity)
        assert component is not None
        assert component["y"] == expected_y
        assert component["y'"] == expected_y_prime
