from numpy import array
from batala.engine.plugin import (
    PluginDependency,
)
from batala.engine.utils import Registry
from batala.systems.system import System

GRAVITY_CONSTANT = 10  # in pixel/second
GRAVITY_CONSTANT_NS = GRAVITY_CONSTANT / (10**-9)  # in pixel/nanosecond
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
            Registry({"Transform2DComponentManagerAPI": "1.0.0"}),
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
        if self.accumulator >= ACCUMULATOR_THRESHOLD:
            steps = self.accumulator // ACCUMULATOR_THRESHOLD
            self.accumulator -= ACCUMULATOR_THRESHOLD * steps
            gravity = array([0, -steps])
            api = self.apis["Transform2DPlugin"]["Transform2DComponentManagerAPI"]
            api.add_constant(gravity)  # type: ignore
