from semver import Version
from batala.engine import ModuleId
from batala.engine.module import Module, ModuleType
from batala.systems.system import System


class TestModule(Module, System):
    _name = "Test"
    _version = Version(1, 0, 0)
    _type = ModuleType.SYSTEM

    def __init__(self):
        self.discrete_steps = 0
        self.continuous_time = 0

    def step(self, delta_time):
        self.discrete_steps += 1
        self.continuous_time += delta_time


def test_name():
    module = TestModule()
    name = module.name
    assert name == "Test"


def test_version():
    module = TestModule()
    version = module.version
    assert version == Version(1, 0, 0)
    assert version > Version(0, 0, 0)
    assert version < Version(1, 0, 1)


def test_moduleId():
    module = TestModule()
    name = module.name
    version = module.version
    moduleId = module.moduleId
    hash = (name.strip().lower() + str(version)).__hash__()
    assert moduleId == hash
    assert moduleId != ModuleId(0)


def test_type():
    module = TestModule()
    type = module.type
    assert type == ModuleType.SYSTEM
    assert type != ModuleType.COMPONENT
    assert type != ModuleType.EXTERNAL


def test_step():
    module = TestModule()
    for i in range(10):
        module.step(60)
        assert module.discrete_steps == i+1
        assert module.continuous_time == (i+1)*60
