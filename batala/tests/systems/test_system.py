from batala.engine.plugin import Plugin
from batala.engine.utils import Registry
from batala.tests.engine.mock import TestPlugin
from batala.tests.systems.mock import TestSystem


test_plugins: Registry[Plugin] = Registry({"TestPlugin": TestPlugin()})


def test_init():
    system = TestSystem()
    system.get_dependencies(test_plugins)
    assert system is not None
    assert isinstance(system, TestSystem)
    assert len(system.apis) > 0


def test_step():
    system = TestSystem()
    system.get_dependencies(test_plugins)
    plugin = test_plugins["TestPlugin"]
    for i in range(10):
        system.step(0)
        assert plugin.step_count == i + 1  # type: ignore
