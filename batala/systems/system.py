from abc import ABC, abstractmethod
from typing import Callable, Mapping

from semver import Version

from batala.engine.plugin import (
    Plugin,
    PluginAPI,
    PluginDependency,
    PluginId,
)
from batala.engine.utils import PluginError, Registry


class SystemAPI(PluginAPI, version=Version(0, 0, 0)):
    step: Callable[[int], None]

    def __init__(self, step: Callable[[int], None]) -> None:
        self.step = step


class System(ABC):
    dependencies: list[PluginDependency]
    apis: Registry[Registry[PluginAPI]]

    def __init__(self, plugins: Registry[Plugin]) -> None:
        self.apis = Registry()
        for dependency in self.dependencies:
            id = dependency.id
            if id not in plugins:
                raise PluginError(
                    None, f"No valid plugin found for dependency: {dependency}"
                )
            try:
                plugin = plugins[id]
                self.apis[id] = dependency.validate_plugin(plugin)
            except PluginError as error:
                raise error

    @abstractmethod
    def step(self, delta_time: int):
        raise NotImplemented
