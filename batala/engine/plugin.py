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
    implemented_apis: Registry[PluginAPI]

    def __init_subclass__(cls, version: Version, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.id = safe_hash(cls.__name__)
        cls.version = version
        cls.plugins.append(cls)
        cls.registry[cls.id] = cls

    def get_api(self, api_type: int | str, match_expr: VersionExpr) -> PluginAPI | None:
        if isinstance(api_type, str):
            api_type = safe_hash(api_type)
        if api_type in self.implemented_apis:
            api = self.implemented_apis[api_type]
            if api.version.match(match_expr):
                return api
        return None

    @classmethod
    def __hash__(cls) -> int:
        return safe_hash(cls.__name__)


@dataclass(frozen=True)
class PluginDependency:
    name: str
    version: VersionExpr
    apis: Registry[VersionExpr]

    @property
    def id(self):
        return safe_hash(self.name)

    def validate_plugin(self, plugin: Plugin) -> Registry[PluginAPI]:
        if self.id != plugin.id or not plugin.version.match(self.version):
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
