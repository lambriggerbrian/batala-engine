from abc import ABC, abstractmethod
from ordered_set import OrderedSet
from semver import Version

from batala.engine.utils import safe_hash


class PluginAPI(ABC):
    id: int
    version: Version

    def __init_subclass__(cls, version: Version, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.id = safe_hash(cls.__name__)
        cls.version = version

    @classmethod
    def __hash__(cls) -> int:
        return safe_hash(cls.__name__)


class Plugin(ABC):
    id: int
    plugins: OrderedSet = OrderedSet([])
    registry: dict[int, type["Plugin"]] = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.id = safe_hash(cls.__name__)
        cls.plugins.append(cls)
        cls.registry[cls.id] = cls

    @abstractmethod
    def get_api(self, id: int, match_expr: str) -> PluginAPI | None:
        raise NotImplementedError

    @classmethod
    def __hash__(cls) -> int:
        return safe_hash(cls.__name__)
