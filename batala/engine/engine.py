import time
from ordered_set import OrderedSet
from batala.components.component_manager import ComponentManagerAPI
from batala.engine.entity import Entity
from batala.engine.entity_manager import EntityManager
from batala.engine.plugin import Plugin, PluginDependency, PluginId
from batala.engine.utils import PluginError, Registry
from batala.systems.system import SystemAPI


class Engine:
    entity_manager: EntityManager
    plugins: Registry[Plugin]
    systems: Registry[SystemAPI]
    component_managers: Registry[ComponentManagerAPI]
    pipeline: OrderedSet[SystemAPI]
    frame_times: list[int]

    def __init__(self, dependencies: list[PluginDependency] = []):
        self.entity_manager = EntityManager()
        self.plugins = Registry()
        self.systems = Registry()
        self.component_managers = Registry()
        self.pipeline = OrderedSet([])
        self.frame_times = []
        for dependency in dependencies:
            self.register_dependency(dependency)

    def register_dependency(self, dependency: PluginDependency):
        id, name = dependency.id, dependency.name
        if id not in Plugin.registry:
            raise PluginError(None, f"No registered plugin found of type: {name}")
        instance = Plugin.registry[id]()
        self.plugins[id] = instance
        apis = dependency.validate_plugin(instance)
        for api in apis.values():
            if isinstance(api, SystemAPI):
                api.get_dependencies(self.plugins)
                self.systems[id] = api
                self.pipeline.append(api)
            if isinstance(api, ComponentManagerAPI):
                self.component_managers[id] = api

    def create_entity(self, components: list[PluginId | str] | None = None) -> Entity:
        if components is None:
            components = []
        entity = self.entity_manager.create()
        for component in components:
            manager = self.component_managers[component]
            manager.register_component(entity)
        return entity

    def step(self, delta_time):
        frame_start = time.time_ns()
        for system in self.pipeline:
            system.step(delta_time)
        frame_end = time.time_ns()
        self.frame_times.append(frame_end - frame_start)
