from typing import Callable
from semver import Version
from batala.engine.plugin import Plugin, PluginAPI
from batala.engine.utils import Registry
from batala.systems.system import SystemAPI
from batala.tests.systems.mock import TestSystem


class TestPluginAPI(PluginAPI, version=Version(1, 0, 0)):
    increase_count: Callable[..., None]

    def __init__(self, increase_count: Callable[..., None]) -> None:
        self.increase_count = increase_count


class TestPlugin(Plugin, version=Version(1, 0, 0)):
    step_count: int

    def __init__(self) -> None:
        self.step_count = 0
        self.implemented_apis = Registry(
            {TestPluginAPI.id: TestPluginAPI(self.increase_count)}
        )

    def increase_count(self):
        self.step_count += 1


class TestSystemPlugin(Plugin, version=Version(1, 0, 0)):
    def __init__(self) -> None:
        self.system = TestSystem()
        self.implemented_apis = Registry(
            {
                "SystemAPI": SystemAPI(
                    get_dependencies=self.system.get_dependencies, step=self.system.step
                )
            }
        )
