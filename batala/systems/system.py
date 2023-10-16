from abc import abstractmethod

from batala.engine import ModuleId
from batala.engine.module import Module


class System():
    _dependencies: list[ModuleId]
    _id_to_dependency: dict[ModuleId, Module] = {}

    @abstractmethod
    def step(self, delta_time):
        raise NotImplemented
