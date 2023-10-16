from abc import ABC, abstractmethod
from enum import Enum
from semver import Version

from batala.engine import ModuleId


class ModuleType(Enum):
    SYSTEM = 0
    COMPONENT = 1
    INPUT = 3
    OUTPUT = 4
    EXTERNAL = 5


class Module(ABC):
    _name: str
    _version: Version
    _moduleId: ModuleId
    _type: ModuleType

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def moduleId(self):
        return hash(self._name.strip().lower()+str(self._version))

    @property
    def type(self):
        return self._type

    @staticmethod
    def generate_moduleId(name: str, version: Version):
        return hash(name.strip().lower()+str(version))
