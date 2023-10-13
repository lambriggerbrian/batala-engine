import pytest
from semver import Version
from batala.engine import ModuleId
from batala.engine.automaton import HybridAutomaton
from batala.engine.module import Module, ModuleType


class TestAutomaton(HybridAutomaton):
    def __init__(self):
        self.discrete_steps = 0
        self.continuous_time = 0

    def discrete_step(self):
        self.discrete_steps += 1

    def continuous_step(self, delta_time):
        self.continuous_time += delta_time


def test_init():
    module = Module("Test", Version(0, 0, 0),
                    ModuleType.SYSTEM, TestAutomaton())
    assert module is not None


def test_name():
    module = Module("Test", Version(0, 0, 0),
                    ModuleType.SYSTEM, TestAutomaton())
    name = module.name
    assert name == "Test"


def test_version():
    module = Module("Test", Version(1, 0, 0),
                    ModuleType.SYSTEM, TestAutomaton())
    version = module.version
    assert version == Version(1, 0, 0)
    assert version > Version(0, 0, 0)
    assert version < Version(1, 0, 1)


def test_moduleId():
    module = Module("Test", Version(0, 0, 0),
                    ModuleType.SYSTEM, TestAutomaton())
    name = module.name
    version = module.version
    moduleId = module.moduleId
    hash = (name.strip().lower() + version.__str__()).__hash__()
    assert moduleId == hash
    assert moduleId != ModuleId(0)


def test_type():
    module = Module("Test", Version(0, 0, 0),
                    ModuleType.SYSTEM, TestAutomaton())
    type = module.type
    assert type == ModuleType.SYSTEM
    assert type != ModuleType.COMPONENT
    assert type != ModuleType.EXTERNAL


def test_get_value():
    module = Module("Test", Version(0, 0, 0),
                    ModuleType.SYSTEM, TestAutomaton())
    assert module.get_attribute("discrete_steps") == 0
    assert module.get_attribute("continuous_time") == 0
    with pytest.raises(AttributeError):
        module.get_attribute("bad_value")


def test_step():
    module = Module("Test", Version(0, 0, 0),
                    ModuleType.SYSTEM, TestAutomaton())
    for i in range(10):
        module.step(60)
        assert module.get_attribute("discrete_steps") == i+1
        assert module.get_attribute("continuous_time") == (i+1)*60
