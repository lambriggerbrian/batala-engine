from batala.engine.engine import Engine
from batala.engine.plugin import PluginDependency
from batala.engine.utils import Registry
from batala.systems.system import SystemAPI
from batala.tests.engine.mock import TestPluginAPI, TestPlugin, TestSystemPlugin

test_engine_dependencies = [
    PluginDependency("TestPlugin", "1.0.0", Registry({"TestPluginAPI": "1.0.0"})),
    PluginDependency("TestSystemPlugin", "1.0.0", Registry({"SystemAPI": "0.0.0"})),
]


def test_init():
    engine = Engine(test_engine_dependencies)
    assert engine is not None
    assert isinstance(engine, Engine)


def test_step():
    engine = Engine(test_engine_dependencies)
    plugin = engine.plugins["TestPlugin"]
    for i in range(10):
        engine.step(0)
        assert len(engine.frame_times) == i + 1
        assert plugin.step_count == i + 1  # type: ignore
