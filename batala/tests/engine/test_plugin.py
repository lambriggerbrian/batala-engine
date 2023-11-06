from typing import Callable
from semver import Version

from batala.engine.plugin import Plugin, PluginAPI


class TestPluginAPI(PluginAPI, version=Version(1, 0, 0)):
    increase_count: Callable[..., None]

    def __init__(self, increase_count: Callable[..., None]) -> None:
        self.increase_count = increase_count


class TestPlugin(Plugin):
    step_count: int
    apis: dict[int, TestPluginAPI]

    def __init__(self) -> None:
        self.step_count = 0
        self.apis = {TestPluginAPI.id: TestPluginAPI(self.increase_count)}

    def get_api(self, id: int, match_expr: str) -> PluginAPI | None:
        if id in self.apis:
            api = self.apis[id]
            if api.version.match(match_expr):
                return api
        return None

    def increase_count(self):
        self.step_count += 1


def test_api_id():
    api = TestPluginAPI(lambda: None)
    assert api is not None
    assert isinstance(api, TestPluginAPI)
    assert TestPluginAPI.id == api.id


def test_init():
    plugin = TestPlugin()
    assert plugin is not None
    assert len(Plugin.plugins) == 1
    assert Plugin.registry[TestPlugin.id] == plugin.__class__


def test_get_api():
    plugin = TestPlugin()
    api = plugin.get_api(TestPluginAPI.id, "<1.0.0")
    assert api is None
    api = plugin.get_api(TestPluginAPI.id, "1.0.0")
    assert isinstance(api, TestPluginAPI)
    api = plugin.get_api(TestPluginAPI.id, ">1.0.0")
    assert api is None


def test_api_hook():
    plugin = TestPlugin()
    api = plugin.get_api(TestPluginAPI.id, "1.0.0")
    assert api is not None
    for i in range(10):
        api.increase_count()  # type: ignore
        assert plugin.step_count == i + 1
