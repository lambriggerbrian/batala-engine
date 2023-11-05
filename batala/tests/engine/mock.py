from semver import Version
from batala.engine.module import Module, ModuleInfo, ModuleType
from batala.systems.system import System


class TestModule(Module, System):
    _info = ModuleInfo("Test", Version(1, 0, 0), ModuleType.SYSTEM)

    def __init__(self):
        self.discrete_steps = 0
        self.continuous_time = 0

    def step(self, delta_time):
        self.discrete_steps += 1
        self.continuous_time += delta_time
