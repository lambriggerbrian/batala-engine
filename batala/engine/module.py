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

    def step(self, delta_time):
        self._module_class.step()
        self._module_class.continuous_step(delta_time)

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def moduleId(self):
        return self._moduleId
