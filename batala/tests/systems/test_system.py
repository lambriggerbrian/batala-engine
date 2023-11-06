from batala.tests.engine.mock import TestPlugin
from batala.tests.systems.mock import TestSystem, test_plugins


def test_init():
    system = TestSystem(test_plugins)
    assert system is not None
    assert len(system.apis) > 0


def test_step():
    system = TestSystem(test_plugins)
    plugin = test_plugins[TestPlugin.id]
    for i in range(10):
        system.step(0)
        assert plugin.step_count == i + 1
