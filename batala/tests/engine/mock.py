from typing import Callable
from semver import Version
from batala.engine.module import Module, ModuleInfo, ModuleType
from batala.engine.plugin import APIType, Plugin, PluginAPI, PluginId, VersionExpr
from batala.engine.utils import Registry
from batala.systems.system import System


class TestModule(Module, System):
    _info = ModuleInfo("Test", Version(1, 0, 0), ModuleType.SYSTEM)

    def __init__(self):
        self.discrete_steps = 0
        self.continuous_time = 0

    def step(self, delta_time):
        self.discrete_steps += 1
        self.continuous_time += delta_time


class TestPluginAPI(PluginAPI, version=Version(1, 0, 0)):
    increase_count: Callable[..., None]

    def __init__(self, increase_count: Callable[..., None]) -> None:
        self.increase_count = increase_count


class TestPlugin(Plugin, version=Version(1, 0, 0)):
    step_count: int

    def __init__(self) -> None:
        self.step_count = 0
        self.apis = Registry({TestPluginAPI.id: TestPluginAPI(self.increase_count)})

    def increase_count(self):
        self.step_count += 1
