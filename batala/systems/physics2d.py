import numpy
from batala.components.transform2d_component_manager import Transform2D
from batala.engine.plugin import (
    PluginAPI,
    PluginDependency,
)
from batala.engine.utils import Registry, clamp
from batala.systems.system import System

WORLD_CONSTRAINT = 595


class Physics2DSystem(System):
    """Base class for systems.
    Has functions meant to fulfill SystemAPI, with an initial
    implementation for get_dependencies.
    """

    dependencies = [
        PluginDependency(
            "Transform2DPlugin",
            "1.0.0",
            Registry({"NdarrayComponentManagerAPI": "1.0.0"}),
        )
    ]

    def __init__(self) -> None:
        super().__init__()
        self.transform2D: PluginAPI | None = None

    def step(self, delta_time: int):
        """Step simulation function.

        Args:
            delta_time (int): the time elapsed in nanoseconds
        """
        dt = delta_time / 10**9
        if self.transform2D is None:  # type: ignore
            self.transform2D = self.apis["Transform2DPlugin"][
                "NdarrayComponentManagerAPI"
            ]
        for instance in self.transform2D.iter():  # type: ignore
            for axis in ("x", "y"):
                first_degree, second_degree, third_degree = (
                    axis,
                    f"{axis}'",
                    f"{axis}''",
                )
                value_prime = instance[third_degree] * dt + instance[second_degree]
                value = value_prime * dt + instance[first_degree]
                instance[second_degree] = value_prime
                instance[first_degree] = value
