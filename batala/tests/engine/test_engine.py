import os
from pathlib import Path
from batala.engine.engine import Engine
from batala.engine.plugin import PluginDependency
from batala.engine.utils import Registry, load_module

test_engine_dependencies = [
    PluginDependency("TestPlugin", "1.0.0", Registry({"TestPluginAPI": "1.0.0"})),
    PluginDependency("TestSystemPlugin", "1.0.0", Registry({"SystemAPI": "0.0.0"})),
]

# Get current path
path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)

module_paths = [Path(dirpath, "mock.py"), Path(dirpath, "../../systems/system.py")]

for module_path in module_paths:
    load_module(module_path)


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
