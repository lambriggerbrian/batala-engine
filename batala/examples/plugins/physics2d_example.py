from semver import Version
from batala.components import component_manager
from batala.components.transform2d_component_manager import (
    Transform2DComponentManager,
    Transform2DComponentManagerAPI,
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
                "Transform2DComponentManagerAPI": Transform2DComponentManagerAPI(
                    register_component=self.component_manager.register_component,
                    get_component=self.component_manager.get_component,
                    update_component=self.component_manager.update_component,
                    assign_component=self.component_manager.assign_component,
                    destroy=self.component_manager.destroy,
                    add_constant=self.component_manager.add_constant,
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
