import pytest
from semver import Version
from batala.engine import ModuleId
from batala.engine.module import Module, ModuleType, ModuleLogic


class TestModuleLogic(ModuleLogic):
    def __init__(self):
        self.discrete_steps = 0
        self.continuous_time = 0

    def discrete_step(self):
        self.discrete_steps += 1

    def continuous_step(self, delta_time):
        self.continuous_time += delta_time

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value


def test_init():
    module = Module("Test", Version(0, 0, 0),
                    ModuleType.SYSTEM, TestModuleLogic())
    assert module is not None


def test_name():
    module = Module("Test", Version(0, 0, 0),
                    ModuleType.SYSTEM, TestModuleLogic())
    name = module.name
    assert name == "Test"


def test_version():
    module = Module("Test", Version(1, 0, 0),
                    ModuleType.SYSTEM, TestModuleLogic())
    version = module.version
    assert version == Version(1, 0, 0)
    assert version > Version(0, 0, 0)
    assert version < Version(1, 0, 1)


def test_moduleId():
    module = Module("Test", Version(0, 0, 0),
                    ModuleType.SYSTEM, TestModuleLogic())
    name = module.name
    version = module.version
    moduleId = module.moduleId
    hash = (name.strip().lower() + str(version)).__hash__()
    assert moduleId == hash
    assert moduleId != ModuleId(0)


def test_type():
    module = Module("Test", Version(0, 0, 0),
                    ModuleType.SYSTEM, TestModuleLogic())
    type = module.type
    assert type == ModuleType.SYSTEM
    assert type != ModuleType.COMPONENT
    assert type != ModuleType.EXTERNAL


def test_get_item():
    module = Module("Test", Version(0, 0, 0),
                    ModuleType.SYSTEM, TestModuleLogic())
    assert module["discrete_steps"] == 0
    assert module["continuous_time"] == 0
    with pytest.raises(KeyError):
        module["bad_value"]


def test_set_item():
    module = Module("Test", Version(0, 0, 0),
                    ModuleType.SYSTEM, TestModuleLogic())
    module["discrete_steps"] = 1
    module["continuous_time"] = 60
    assert module["discrete_steps"] == 1
    assert module["continuous_time"] == 60


def test_step():
    module = Module("Test", Version(0, 0, 0),
                    ModuleType.SYSTEM, TestModuleLogic())
    for i in range(10):
        module.step(60)
        assert module["discrete_steps"] == i+1
        assert module["continuous_time"] == (i+1)*60
