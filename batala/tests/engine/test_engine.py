import time
from semver import Version
from batala.engine.engine import Engine
from batala.engine.module import Module, ModuleLogic, ModuleType


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


test_module = Module("TestModule", Version(0, 0, 0),
                     ModuleType.SYSTEM, TestModuleLogic())


def test_init():
    engine = Engine([test_module])
    assert engine is not None
    assert isinstance(engine, Engine)


def test_register_module():
    engine = Engine()
    engine.register_module(test_module)
    moduleId = test_module.moduleId
    module = engine.modules[moduleId]
    logic = engine.systems[moduleId]
    assert module == test_module
    assert logic == test_module.logic


def test_step():
    engine = Engine([test_module])
    moduleId = test_module.moduleId
    for i in range(10):
        engine.step(60)
        assert engine.modules[moduleId]["discrete_steps"] == i+1
        assert engine.modules[moduleId]["continuous_time"] == (i+1)*60
        assert engine.frame_times[i] is not None
        assert engine.module_times[moduleId][i] is not None
