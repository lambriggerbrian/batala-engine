from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Any
from semver import Version

from batala.engine import ModuleId


class ModuleType(Enum):
    ENTITY = 0
    COMPONENT = 1
    SYSTEM = 2
    GROUP = 3


def generate_moduleId(name: str, version: Version):
    return hash(name.strip().lower() + str(version))


@dataclass(frozen=True)
class ModuleInfo:
    name: str
    version: Version
    type: ModuleType

    @property
    def moduleId(self):
        return ModuleId(self.__hash__())

    def __hash__(self) -> int:
        return generate_moduleId(self.name, self.version)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, ModuleInfo) and __value.moduleId == self.moduleId


class Module(ABC):
    _info: ModuleInfo
    _infoKeys: tuple[str, str, str, str] = ("name", "version", "type", "moduleId")

    def get_info(self, name: str) -> Any:
        if name in self._infoKeys:
            return self._info.__getattribute__(name)
