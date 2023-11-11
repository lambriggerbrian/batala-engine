from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import yaml

from batala.engine import DEFAULT_SEARCH_PATHS
from batala.engine.plugin import PluginDependency


@dataclass(frozen=True)
class EngineConfig:
    search_paths: list[Path]
    dependencies: list[PluginDependency]

    @staticmethod
    def parse(config: dict) -> "EngineConfig":
        additional_paths = [Path(i) for i in config.get("search_paths", [])]
        search_paths = DEFAULT_SEARCH_PATHS + additional_paths
        dependencies = [
            PluginDependency.parse(i) for i in config.get("dependencies", [])
        ]
        return EngineConfig(search_paths, dependencies)


class Loader(ABC):
    @abstractmethod
    def load(self) -> EngineConfig:
        raise NotImplementedError


class YamlLoader(Loader):
    def __init__(self, file) -> None:
        self.path = Path(file)

    def load(self) -> EngineConfig:
        with open(self.path, "r") as file:
            config = yaml.safe_load(file)
            return EngineConfig.parse(config)
