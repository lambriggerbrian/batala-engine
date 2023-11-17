import numpy
from batala.components.transform2d_component_manager import Transform2D
from batala.engine.plugin import (
    PluginDependency,
)
from batala.engine.utils import Registry
from batala.systems.system import System

GRAVITY_CONSTANT = 10  # in pixel/second
GRAVITY_CONSTANT_NS = GRAVITY_CONSTANT / (10**-9)  # in pixel/nanosecond
GRAVITY_CONSTANT_ARRAY = numpy.array((0, 0, 0, 1, 0, 0), dtype=Transform2D)
ACCUMULATOR_THRESHOLD = 10**8  # number of nanoseconds per 1 pixel movement


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
        self.accumulator = 0

    def step(self, delta_time: int):
        """Step simulation function.

        Args:
            delta_time (int): the time elapsed in nanoseconds
        """
        self.accumulator += delta_time
        transform2D = self.apis["Transform2DPlugin"]["NdarrayComponentManagerAPI"]
        delta_gravity = 0
        if self.accumulator >= ACCUMULATOR_THRESHOLD:
            steps = self.accumulator // ACCUMULATOR_THRESHOLD
            self.accumulator -= ACCUMULATOR_THRESHOLD * steps
            delta_gravity = steps
        for instance in transform2D.iter():  # type: ignore
            y_prime = instance["y'"] + delta_gravity
            instance["y'"] += delta_gravity
            instance["y"] = instance["y"] + y_prime
