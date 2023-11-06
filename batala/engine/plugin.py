from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Mapping, TypeVar
from ordered_set import OrderedSet
from semver import Version

from batala.engine.utils import PluginError, Registry, safe_hash

APIType = int
PluginId = int
VersionExpr = str


class PluginAPI(ABC):
    apis: OrderedSet = OrderedSet([])
    registry: Registry[type["PluginAPI"]] = Registry()
    id: APIType
    version: Version

    def __init_subclass__(cls, version: Version, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.id = safe_hash(cls.__name__)
        cls.version = version
        cls.apis.append(cls)
        cls.registry[cls.id] = cls

    @classmethod
    def __hash__(cls) -> int:
        return safe_hash(cls.__name__)


class Plugin(ABC):
    plugins: OrderedSet = OrderedSet([])
    registry: Registry[type["Plugin"]] = Registry()
    id: PluginId
    version: Version

    def __init_subclass__(cls, version: Version, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.id = safe_hash(cls.__name__)
        cls.version = version
        cls.plugins.append(cls)
        cls.registry[cls.id] = cls

    @abstractmethod
    def get_api(self, type: APIType, match_expr: VersionExpr) -> PluginAPI | None:
        raise NotImplementedError

    @classmethod
    def __hash__(cls) -> int:
        return safe_hash(cls.__name__)


@dataclass(frozen=True)
class PluginDependency:
    pluginId: PluginId
    pluginVersion: VersionExpr
    apis: Registry[VersionExpr]

    def validate_plugin(self, plugin: Plugin) -> Registry[PluginAPI]:
        if self.pluginId != plugin.id or not plugin.version.match(self.pluginVersion):
            raise PluginError(plugin, "Incorrect plugin type or version.")
        valid_apis: Registry[PluginAPI] = Registry()
        invalid_apis = []
        for api, version in self.apis.items():
            valid_api = plugin.get_api(api, version)
            if valid_api:
                valid_apis[api] = valid_api
            else:
                invalid_apis.append((api, version))
        if len(invalid_apis) > 0:
            raise PluginError(plugin, f"Invalid API dependencies: {invalid_apis}")
        return valid_apis
