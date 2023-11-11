from batala.engine.plugin import PluginDependency
from batala.engine.utils import Registry
from batala.systems.system import System


class TestSystem(System):
    dependencies = [
        PluginDependency("TestPlugin", "1.0.0", Registry({"TestPluginAPI": "1.0.0"}))
    ]

    def step(self, delta_time: int):
        self.apis["TestPlugin"]["TestPluginAPI"].increase_count()  # type: ignore
