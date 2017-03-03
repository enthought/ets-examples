
import numpy as np

from enable.tools.api import ValueDragTool
from traits.api import Any

class OffsetDragTool(ValueDragTool):

    x_mapper = lambda x: x

    y_mapper = lambda y: y

    def get_value(self):
        return np.array(self.component.offset)

    def set_delta(self, value, delta_x, delta_y):
        self.component.offset = tuple(self.original_value + np.array([delta_x, delta_y]))
