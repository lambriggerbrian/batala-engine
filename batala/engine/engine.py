from ordered_set import OrderedSet
from batala.components.component_manager import ComponentManager
from batala.engine import ModuleId
from batala.engine.entity_manager import EntityManager
from batala.engine.module import Module
from batala.systems.system import System


class Engine():
    entity_manager: EntityManager
    modules: dict[ModuleId, Module]
    systems: dict[ModuleId, System]
    component_managers: dict[ModuleId, ComponentManager]
    external: dict[ModuleId, Module]
    pipeline: OrderedSet[Module]

    def __init__(self, modules: list[Module]) -> None:
        pass
