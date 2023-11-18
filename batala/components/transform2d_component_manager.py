from numpy import dtype, float64

from batala.components.ndarray_component_manager import (
    NdarrayComponentManager,
)


Transform2D = dtype(
    [
        ("x", float64),
        ("y", float64),
        ("x'", float64),
        ("y'", float64),
        ("x''", float64),
        ("y''", float64),
    ]
)


class Transform2DComponentManager(NdarrayComponentManager):
    component_type = Transform2D

    def __init__(self):
        super().__init__(self.component_type)
