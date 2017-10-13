
from bisect import bisect_right, bisect_left

from numpy import clip

from enable.api import BaseTool
from traits.api import Float, List, Property, cached_property

# default zoom levels
ZOOM_STEPS = [1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0]
ZOOM_STEPS = [1.0/x for x in ZOOM_STEPS[:0:-1]] + ZOOM_STEPS


class ScaleZoomTool(BaseTool):
    """ A tool which changes the scale on mouse wheel events. """

    #: The amount to zoom per wheel click (15 degrees)
    zoom_scale = Float(1.125)

    #: The maximum permitted zoom.
    scale_steps = List(Float, ZOOM_STEPS)

    #: The maximum permitted zoom.
    max_scale = Property(Float, depends_on='scale_steps[]')

    #: The minimum permitted zoom.
    min_scale = Property(Float, depends_on='scale_steps[]')

    def normal_mouse_wheel(self, event):
        """ Zoom using the mouse wheel. """
        zoom_factor = 1.0 + (event.mouse_wheel*self.zoom_scale)
        new_scale = self.component.scale * zoom_factor
        scale = clip(new_scale, self.min_scale, self.max_scale)
        self.component.rescale(scale, (event.x, event.y))
        event.handled = True

    def normal_key_pressed(self, event):
        """ Zoom using '+' or '-' keys. """
        if event.alt_down or event.control_down:
            return

        if event.character == '=' or event.character == '+':
            zoom_index = bisect_right(self.scale_steps, self.component.scale)
            if zoom_index >= len(self.scale_steps):
                return
            new_scale = self.scale_steps[zoom_index]
        elif event.character == '-':
            zoom_index = bisect_left(self.scale_steps, self.component.scale)-1
            if zoom_index < 0:
                return
            new_scale = self.scale_steps[zoom_index]
        else:
            return

        self.component.rescale(new_scale)
        event.handled = True

    @cached_property
    def _get_max_scale(self):
        return max(self.scale_steps)

    @cached_property
    def _get_min_scale(self):
        return min(self.scale_steps)
