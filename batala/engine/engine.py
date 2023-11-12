import logging
import time
from ordered_set import OrderedSet
from batala.components.component_manager import ComponentManagerAPI
from batala.engine import Id
from batala.engine.entity import Entity
from batala.engine.entity_manager import EntityManager
from batala.engine.loader import EngineConfig
from batala.engine.plugin import Plugin, PluginDependency, PluginId
from batala.engine.utils import BatalaError, PluginError, Registry
from batala.systems.system import SystemAPI


logger = logging.getLogger(__name__)


class Engine:
    """The main Engine class
    Registers plugins, entities, components, and systems, then uses their exposed APIs
    to run the main game loop with the step function
    """

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

    @staticmethod
    def from_config(config: EngineConfig) -> "Engine":
        return Engine(config.dependencies)

    def register_dependency(self, dependency: PluginDependency):
        """Register a dependency by instantiating an instance of its plugin.
        Checks the Plugin class registry for a plugin that matches the dependency.
        If one is found, the plugin is instantiated, and its APIs are registered with
        the Engine.

        Args:
            dependency (PluginDependency): the dependency to instantiate and register

        Raises:
            PluginError: if no valid plugin matches the dependency
        """
        id, name = dependency.id, dependency.name
        if id not in Plugin.registry:
            error = PluginError(None, f"No registered plugin found of type: {name}")
            logger.exception(error)
            raise error
        instance = Plugin.registry[id]()
        self.plugins[id] = instance
        apis = dependency.validate_plugin(instance)
        for api in apis.values():
            if isinstance(api, SystemAPI):
                api.get_dependencies(self.plugins)
                self.systems[id] = api
                self.pipeline.append(api)
                logger.info(
                    "SystemAPI registered'{}'({})".format(
                        dependency.name, dependency.version
                    )
                )
            if isinstance(api, ComponentManagerAPI):
                self.component_managers[id] = api
                logger.info(
                    "ComponentManagerAPI registered'{}'({})".format(
                        dependency.name, dependency.version
                    )
                )

    def create_entity(self) -> Entity:
        """Creates and registers an Entity.

        Returns:
            Entity: the created entity
        """
        entity = self.entity_manager.create()
        logger.info("Entity({}) created".format(entity))
        return entity

    def destroy_entity(self, entity: Entity | Id) -> bool:
        """Destroy an entity.

        Args:
            entity (Entity): entity or ID of entity to destroy

        Returns:
            bool: True if entity is alive and destroyed successfully, else None
        """
        managed_entity = self.entity_manager[entity]
        if managed_entity is None:
            return False
        self.entity_manager.destroy(managed_entity)
        logger.info("Entity({}) destroyed".format(entity))
        for manager in self.component_managers.values():
            manager.destroy(managed_entity)
        return True

    def register_components(self, entity: Entity, components: list[PluginId | str]):
        """Register a list of components for an entity.

        Args:
            entity (Entity): the entity to own components
            components (list[PluginId | str]): ids or str names of ComponentManager
                                               plugins to register with

        Raises:
            BatalaError: if no matching ComponentManager is found for a member of list
        """
        for component in components:
            manager = self.component_managers.get_value(component)
            if not manager:
                error = BatalaError(f"No valid Component Manager registered to Engine.")
                logger.exception(error)
                raise error
            manager.register_component(entity)
            logger.info(
                "Entity({}) registered component with Plugin({})".format(
                    entity, component
                )
            )

    def step(self, delta_time: int):
        """Step forward main simulation.
        Records the start and end times of the step, calling the step function of each
        registered system.

        Args:
            delta_time (int): time to simulate (in ns)
        """
        if delta_time < 0:
            error = ValueError(f"delta_time must be a positive integer")
            logger.exception(error)
            raise error
        frame_number = len(self.frame_times)
        frame_start = time.time_ns()
        logger.info("Frame {} started".format(frame_number))
        for system in self.pipeline:
            system.step(delta_time)
        frame_end = time.time_ns()
        duration = frame_end - frame_start
        self.frame_times.append(duration)
        logger.info("Frame {} ended ({}ns)".format(frame_number, duration))
