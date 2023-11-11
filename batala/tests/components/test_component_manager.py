from batala.engine import Generation, Index
from batala.engine.entity import Entity
from batala.examples.classes.component_examples import TestComponentManager

test_entity = Entity(Index(0), Generation(0))
other_entity = Entity(Index(1), Generation(0))


def test_init():
    component_manager = TestComponentManager()
    assert component_manager is not None
    assert isinstance(component_manager, TestComponentManager)


def test_register_component():
    component_manager = TestComponentManager()
    component_manager.register_component(test_entity)


def test_get_component():
    component_manager = TestComponentManager()
    component_manager.register_component(test_entity)
    component = component_manager.get_component(test_entity)
    assert component is not None
    assert component["discrete_steps"] == 0
    assert component["continuous_time"] == 0


def test_update_component():
    component_manager = TestComponentManager()
    component_manager.register_component(test_entity)
    component = component_manager.update_component(test_entity, "discrete_steps", 1)
    assert component is not None
    assert component["discrete_steps"] == 1
    assert component["continuous_time"] == 0


def test_destroy():
    component_manager = TestComponentManager()
    component_manager.register_component(test_entity)
    assert not component_manager.destroy(other_entity)
    assert component_manager.destroy(test_entity)
    assert component_manager.get_component(test_entity) is None


def test_iter():
    component_manager = TestComponentManager()
    component_manager.register_component(test_entity)
    component_manager.register_component(other_entity)
    count = 0
    for _ in component_manager:
        count += 1
    assert count == 2
