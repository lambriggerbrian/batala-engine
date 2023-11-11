from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import yaml
from batala import PACKAGE_PATH

from batala.engine import DEFAULT_SEARCH_PATHS
from batala.engine.plugin import PluginDependency
from batala.engine.utils import load_path


SPECIAL_PATHS = {"PACKAGE_PATH": PACKAGE_PATH}


def resolve_path(path_str: str) -> Path:
    resolved_path = path_str
    for key, value in SPECIAL_PATHS.items():
        resolved_path = resolved_path.replace(key, value)
    return Path(resolved_path)


@dataclass(frozen=True)
class EngineConfig:
    search_paths: list[Path]
    dependencies: list[PluginDependency]

    @staticmethod
    def parse(config: dict) -> "EngineConfig":
        additional_paths = [resolve_path(i) for i in config.get("search_paths", [])]
        search_paths = DEFAULT_SEARCH_PATHS + additional_paths
        dependencies = [
            PluginDependency.parse(i) for i in config.get("dependencies", [])
        ]
        return EngineConfig(search_paths, dependencies)


class Loader(ABC):
    @abstractmethod
    def load(self) -> EngineConfig:
        raise NotImplementedError

    def import_modules(self):
        config = self.load()
        for path in config.search_paths:
            load_path(path)


class YamlLoader(Loader):
    def __init__(self, target: str | Path) -> None:
        if isinstance(target, str):
            self.path = Path(target)
        else:
            self.path = target

    def load(self) -> EngineConfig:
        with open(self.path, "r") as file:
            config = yaml.safe_load(file)
            return EngineConfig.parse(config)
