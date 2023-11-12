from batala.components.transform2d_component_manager import (
    Transform2DComponentManager,
    Transform2DComponentManagerAPI,
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
    api = Transform2DComponentManagerAPI(add_constant=component_manager.add_constant)
    system.apis = Registry(
        {"Transform2DPlugin": Registry({"Transform2DComponentManagerAPI": api})}
    )
    for i in range(10):
        expected_y = (i + 1) // 2 * -1
        system.step(half_step)
        component = component_manager.get_component(test_entity)
        assert component is not None
        assert component["y"] == expected_y
