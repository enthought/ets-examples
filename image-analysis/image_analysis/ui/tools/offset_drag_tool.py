
import numpy as np

from enable.tools.api import ValueDragTool

identity = lambda x: x

class OffsetDragTool(ValueDragTool):
    """ A drag tool that changes the offset of a component. """

    #: The mapper between screen and offset x coords: default is no change.
    x_mapper = identity

    #: The mapper between screen and offset y coords: default is no change.
    y_mapper = identity

    def get_value(self):
        """ Get the value being modified. """
        return np.array(self.component.offset)

    def set_delta(self, value, delta_x, delta_y):
        """ Set the value from a provided delta. """
        new_value = tuple(self.original_value + np.array([delta_x, delta_y]))
        self.component.offset = new_value
