from numpy import dtype, int16

from batala.components.ndarray_component_manager import (
    NdarrayComponentManager,
)


Transform2D = dtype(
    [
        ("x", int16),
        ("y", int16),
        ("x'", int16),
        ("y'", int16),
        ("x''", int16),
        ("y''", int16),
    ]
)


class Transform2DComponentManager(NdarrayComponentManager):
    component_type = Transform2D

    def __init__(self):
        super().__init__(self.component_type)
