from abc import ABC, abstractmethod
from enum import Enum
from semver import Version

from batala.engine import ModuleId
from batala.engine.automaton import HybridAutomaton


class ModuleType(Enum):
    SYSTEM = 0
    COMPONENT = 1
    EXTERNAL = 2


class ModuleLogic(ABC):
    @abstractmethod
    def discrete_step(self):
        raise NotImplemented

    @abstractmethod
    def continuous_step(self, delta_time):
        raise NotImplemented

    @abstractmethod
    def __getitem__(self, key):
        raise NotImplemented

    @abstractmethod
    def __setitem__(self, key, value):
        raise NotImplemented


class Module():
    _name: str
    _version: Version
    _moduleId: ModuleId
    _type: ModuleType
    _logic: ModuleLogic

    def __init__(self, name: str, version: Version, type: ModuleType, module_logic: ModuleLogic):
        self._name = name
        self._version = version
        self._type = type
        self._logic = module_logic
        self._moduleId = hash(name.strip().lower()+str(version))

    def step(self, delta_time):
        self._logic.discrete_step()
        self._logic.continuous_step(delta_time)

    def __getitem__(self, key):
        return self._logic[key]

    def __setitem__(self, key, value):
        self._logic[key] = value

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def moduleId(self):
        return self._moduleId

    @property
    def type(self):
        return self._type

    @property
    def logic(self):
        return self._logic
