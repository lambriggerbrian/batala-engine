from abc import ABC, abstractmethod
from typing import Callable

from semver import Version

from batala.engine.plugin import (
    Plugin,
    PluginAPI,
    PluginDependency,
)
from batala.engine.utils import PluginError, Registry


class SystemAPI(PluginAPI, version=Version(0, 0, 0)):
    get_dependencies: Callable[[Registry[Plugin]], None]
    step: Callable[[int], None]

    def __init__(
        self,
        get_dependencies: Callable[[Registry[Plugin]], None],
        step: Callable[[int], None],
    ) -> None:
        self.get_dependencies = get_dependencies
        self.step = step


class System(ABC):
    dependencies: list[PluginDependency]
    apis: Registry[Registry[PluginAPI]]

    def __init__(self) -> None:
        self.apis = Registry()

    def get_dependencies(self, plugins: Registry[Plugin]):
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
