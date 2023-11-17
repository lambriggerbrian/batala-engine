from semver import Version
from batala.components.ndarray_component_manager import NdarrayComponentManagerAPI
from batala.components.transform2d_component_manager import (
    Transform2DComponentManager,
)
from batala.engine.plugin import Plugin, PluginAPI
from batala.engine.utils import Registry
from batala.systems.physics2d import Physics2DSystem
from batala.systems.system import SystemAPI


class Transform2DPlugin(Plugin, version=Version(1, 0, 0)):
    def __init__(self) -> None:
        self.component_manager = Transform2DComponentManager()
        self.implemented_apis: Registry[PluginAPI] = Registry(
            {
                "NdarrayComponentManagerAPI": NdarrayComponentManagerAPI(
                    register_component=self.component_manager.register_component,
                    get_component=self.component_manager.get_component,
                    update_component=self.component_manager.update_component,
                    assign_component=self.component_manager.assign_component,
                    destroy=self.component_manager.destroy,
                    iter=self.component_manager.__iter__,
                ),
            }
        )


class Physics2DPlugin(Plugin, version=Version(1, 0, 0)):
    def __init__(self) -> None:
        self.system = Physics2DSystem()
        self.implemented_apis: Registry[PluginAPI] = Registry(
            {
                "SystemAPI": SystemAPI(
                    get_dependencies=self.system.get_dependencies, step=self.system.step
                ),
            }
        )
