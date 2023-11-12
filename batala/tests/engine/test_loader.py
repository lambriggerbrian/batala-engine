import os
from pathlib import Path
import sys

from batala import PACKAGE_PATH
from batala.engine.engine import Engine
from batala.engine.loader import EngineConfig, YamlLoader
from batala.engine.plugin import Plugin


path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)
test_config = Path(PACKAGE_PATH, "examples/configs/step_test.yaml")
example_path = Path(PACKAGE_PATH, "examples/plugins/engine_examples.py")


def test_yamlloader_init():
    loader = YamlLoader(test_config)
    assert isinstance(loader, YamlLoader)
    assert loader.path == test_config


def test_yamlloader_load():
    loader = YamlLoader(test_config)
    config = loader.load()
    assert isinstance(config, EngineConfig)
    assert config.search_paths[2] == example_path
    assert len(config.dependencies) == 2


def test_yamlloader_import():
    loader = YamlLoader(test_config)
    loader.import_modules()
    assert "engine_examples" in sys.modules
    plugin = Plugin.registry["TestPlugin"]
    assert plugin is not None


def test_engineconfig():
    loader = YamlLoader(test_config)
    config = loader.load()
    loader.import_modules()
    engine = Engine.from_config(config)
    assert isinstance(engine, Engine)
    assert engine.plugins["TestPlugin"] is not None
    assert engine.systems["TestSystemPlugin"] is not None
