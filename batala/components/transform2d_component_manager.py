from dataclasses import dataclass
from typing import Any, Callable
from numpy import dtype, int16
from semver import Version
from batala.components.component import Component
from batala.components.component_manager import ComponentManagerAPI

from batala.components.ndarray_component_manager import (
    NdarrayComponent,
    NdarrayComponentManager,
)
from batala.engine.entity import Entity
from batala.engine.plugin import PluginAPI


Transform2D = dtype([("x", int16), ("y", int16)])


@dataclass(frozen=True)
class Transform2DComponentManagerAPI(ComponentManagerAPI, version=Version(1, 0, 0)):
    register_component: Callable[[Entity], bool]
    get_component: Callable[[Entity], Component | None]
    update_component: Callable[[Entity, str, Any], Component | None]
    assign_component: Callable[[Entity, NdarrayComponent], bool]
    destroy: Callable[[Entity], bool]
    add_constant: Callable[[str, Any], None]


class Transform2DComponentManager(NdarrayComponentManager):
    component_type = Transform2D

    def __init__(self):
        super().__init__(self.component_type)

    def add_constant(self, field: str, constant: Any):
        for i in range(self.count):
            self.instances[i][field] += constant
