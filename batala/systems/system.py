from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable
from semver import Version

from batala.engine.plugin import (
    Plugin,
    PluginAPI,
    PluginDependency,
)
from batala.engine.utils import PluginError, Registry


@dataclass(frozen=True)
class SystemAPI(PluginAPI, version=Version(0, 0, 0)):
    """ComponentManager API instance to pass to other systems.
    A frozen dataclass for immutability and automated __init__.
    """

    get_dependencies: Callable[[Registry[Plugin]], None]
    step: Callable[[int], None]


class System(ABC):
    """Base class for systems.
    Has functions meant to fulfill the above SystemAPI,
    with an initial implementation for get_dependencies.
    """

    dependencies: list[PluginDependency]
    apis: Registry[Registry[PluginAPI]]

    def __init__(self) -> None:
        self.apis = Registry()

    def get_dependencies(self, plugins: Registry[Plugin]):
        """Populate needed APIs from a registry of plugins.

        Args:
            plugins (Registry[Plugin]): list of available plugins and their APIs

        Raises:
            PluginError: if required plugin is not in plugins
        """
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
        """Step gameloop function.

        Args:
            delta_time (int): the time elapsed in nanoseconds
        """
        raise NotImplemented
