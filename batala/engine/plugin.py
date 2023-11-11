from abc import ABC
from dataclasses import dataclass
import logging
from ordered_set import OrderedSet
from semver import Version

from batala.engine.utils import PluginError, Registry, safe_hash

APIType = int
PluginId = int
VersionExpr = str
logger = logging.getLogger(__name__)


class PluginAPI(ABC):
    """Base class for APIs
    Does some class-level initialization/registering with __init_subclass__
    and overrides hash function to use safe_hash of class name.
    See engine.utils.safe_hash() for implementation.
    """

    # Values handled in __init_subclass__
    apis: OrderedSet = OrderedSet([])
    registry: Registry[type["PluginAPI"]] = Registry()
    id: APIType

    # Initialized by derived classes with DerivedClass(PluginAPI, version=VERSION)
    version: Version

    def __init_subclass__(cls, version: Version, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.id = safe_hash(cls.__name__)
        cls.version = version
        cls.apis.append(cls)
        cls.registry[cls.id] = cls
        logger.info("PluginAPI registered '{}'({})".format(cls.__name__, version))

    @classmethod
    def __hash__(cls) -> int:
        """Use sanitized name and MD5 to give reproducible hashes
        See engine.utils.safe_hash() for implementation.
        """
        return safe_hash(cls.__name__)


class Plugin(ABC):
    """Base class for Plugins
    Does some class-level initialization/registering with __init_subclass__
    and overrides hash function to use safe_hash of class name.
    Enables querying for an implemented API with the id and version.
    """

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
        logger.info("Plugin registered '{}'({})".format(cls.__name__, version))

    def get_api(self, api_type: int | str, match_expr: VersionExpr) -> PluginAPI | None:
        """Get an implemented API from the plugin
        Uses engine.utils.safe_hash to convert a str parameter to int.

        Args:
            api_type (int | str): int or str id representing the requested API
            match_expr (VersionExpr): str expression of required API version,
                                      (see semver Version matching for details)

        Returns:
            PluginAPI | None: The requested API or None if not found
        """
        if isinstance(api_type, str):
            api_type = safe_hash(api_type)
        if api_type in self.implemented_apis:
            api = self.implemented_apis[api_type]
            if api.version.match(match_expr):
                return api
        return None

    @classmethod
    def __hash__(cls) -> int:
        """Use sanitized name and MD5 to give reproducible hashes
        See engine.utils.safe_hash() for implementation.
        """
        return safe_hash(cls.__name__)


@dataclass(frozen=True)
class PluginDependency:
    """Dataclass representing a dependency
    A dependency is made up of the name of the desired Plugin, the version of that
    plugin, and a dict-like Registry of API ids to their desired versions.
    """

    name: str
    version: VersionExpr
    apis: Registry[VersionExpr]

    @staticmethod
    def parse(config: dict) -> "PluginDependency":
        name = config["name"]
        version = config["version"]
        apis: Registry[VersionExpr] = Registry(config["apis"])
        return PluginDependency(name, version, apis)

    @property
    def id(self):
        return safe_hash(self.name)

    def validate_plugin(self, plugin: Plugin) -> Registry[PluginAPI]:
        """Validate whether a plugin meets fulfills this dependency
        To be valid, a plugin must match this dependency's name, version, and implement
        all APIs (with specified versions) listed the dict-like Registry 'apis'

        Args:
            plugin (Plugin): the plugin to validate

        Raises:
            PluginError: if plugin or implemented APIs do not match the dependency

        Returns:
            Registry[PluginAPI]: a dict-like registry of APIs matching this dependency
        """
        if self.id != plugin.id or not plugin.version.match(self.version):
            error = PluginError(plugin, "Incorrect plugin type or version.")
            logger.exception(error)
            raise error
        valid_apis: Registry[PluginAPI] = Registry()
        invalid_apis = []
        for api, version in self.apis.items():
            valid_api = plugin.get_api(api, version)
            if valid_api:
                valid_apis[api] = valid_api
            else:
                invalid_apis.append((api, version))
        if len(invalid_apis) > 0:
            error = PluginError(plugin, f"Invalid API dependencies: {invalid_apis}")
            logger.exception(error)
            raise error
        return valid_apis
