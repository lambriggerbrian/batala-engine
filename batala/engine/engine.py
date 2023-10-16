import time
from ordered_set import OrderedSet
from batala.components.component_manager import ComponentManager
from batala.engine import ModuleId
from batala.engine.entity import Entity
from batala.engine.entity_manager import EntityManager
from batala.engine.module import Module, ModuleType
from batala.systems.system import System


class Engine():
    entity_manager: EntityManager
    modules: dict[ModuleId, Module] = {}
    systems: dict[ModuleId, System] = {}
    component_managers: dict[ModuleId, ComponentManager] = {}
    pipeline: OrderedSet[Module] = OrderedSet()
    frame_times: list[int] = []
    module_times: dict[ModuleId, list[int]] = {}

    def __init__(self, modules: list[Module] = []):
        self.entity_manager = EntityManager()
        for module in modules:
            self.register_module(module)

    def register_module(self, module: Module):
        id = module.moduleId
        type = module.type
        self.modules[id] = module
        match type:
            case ModuleType.SYSTEM:
                self.systems[id] = module
                self.module_times[id] = []
                for id in module._dependencies:
                    module._id_to_dependency[id] = self.modules[id]
                self.pipeline.add(module)
            case ModuleType.COMPONENT:
                self.component_managers[id] = module

    def create_entity(self, components: list[ModuleId] = []) -> Entity:
        entity = self.entity_manager.create()
        component_managers = [self.component_managers[moduleId]
                              for moduleId in components]
        for manager in component_managers:
            manager.register_component(entity)
        return entity

    def step(self, delta_time):
        frame_start = time.time_ns()
        for module in self.pipeline:
            id = module.moduleId
            start_time = time.time_ns()
            module.step(delta_time)
            end_time = time.time_ns()
            self.module_times[id].append(start_time - end_time)
        frame_end = time.time_ns()
        self.frame_times.append(frame_end - frame_start)
