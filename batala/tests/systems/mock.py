from batala.engine.plugin import Plugin, PluginDependency
from batala.engine.utils import Registry
from batala.systems.system import System
from batala.tests.engine.mock import TestPlugin, TestPluginAPI

test_plugins: Registry[Plugin] = Registry({TestPlugin.id: TestPlugin()})
test_dependency = PluginDependency(
    TestPlugin.id, "1.0.0", Registry({TestPluginAPI.id: "1.0.0"})
)


class TestSystem(System):
    dependencies = [test_dependency]

    def __init__(self, plugins: Registry[Plugin]) -> None:
        super().__init__(plugins)

    def step(self, delta_time: int):
        self.apis["TestPlugin"]["TestPluginAPI"].increase_count()  # type: ignore
