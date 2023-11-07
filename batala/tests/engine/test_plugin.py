from batala.tests.engine.mock import TestPlugin, TestPluginAPI


def test_api_id():
    api = TestPluginAPI(lambda: None)
    assert api is not None
    assert isinstance(api, TestPluginAPI)
    assert TestPluginAPI.id == api.id


def test_init():
    plugin = TestPlugin()
    assert plugin is not None
    assert isinstance(plugin, TestPlugin)


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
