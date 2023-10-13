from enum import Enum
from semver import Version

from batala.engine import ModuleId
from batala.engine.automaton import HybridAutomaton


class ModuleType(Enum):
    SYSTEM = 0
    COMPONENT = 1
    EXTERNAL = 2


class Module():
    _name: str
    _version: Version
    _moduleId: ModuleId
    _type: ModuleType
    _module_class: HybridAutomaton

    def __init__(self, name: str, version: Version, type: ModuleType, module_class: HybridAutomaton):
        self._name = name
        self._version = version
        self._type = type
        self._module_class = module_class
        self._moduleId = hash(name.strip().lower()+version.__str__())

    def step(self, delta_time):
        self._module_class.discrete_step()
        self._module_class.continuous_step(delta_time)

    def get_attribute(self, name: str):
        return self._module_class.__getattribute__(name)

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
