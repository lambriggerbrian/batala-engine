from numpy import dtype, uint16

from batala.components.ndarray_component_manager import NdarrayComponentManager


Transform2D = dtype([("x", uint16), ("y", uint16)])


class Transform2DComponentManager(NdarrayComponentManager):
    component_type = Transform2D

    def __init__(self):
        super().__init__(self.component_type)
