
from future.builtins import super

import numpy as np

from chaco.abstract_colormap import AbstractColormap
from enable.api import Component
from traits.api import ArrayOrNone, Bool, Float, Instance, Int, Tuple, on_trait_change

from image_analysis.model.i_image_data import IImageData


class ImageDataComponent(Component):
    """ An Enable component that displays an IImageData instance """

    #: The image data to display.
    image_data = Instance(IImageData, invalidate_cache=True)

    #: The scale factor of the image display.
    scale = Float(1.0, invalidate_visible_cache=True)

    #: The x, y offset of the bottom left of the image relative to the top left
    #: of the component.
    offset = Tuple(Float, Float, invalidate_visible_cache=True)

    #: The color map to use for the display when not using RGB.
    color_map = Instance(AbstractColormap, invalidate_cache=True)

    #: The time-index of the image being displayed
    time_index = Int(0, invalidate_visible_cache=True)

    #: The plane-index of the image being displayed
    plane_index = Int(0, invalidate_visible_cache=True)

    #: Whether or not the raw image cache is valid
    _cache_valid = Bool

    #: A cache of the full colormapped image.
    _cached_image = ArrayOrNone(shape=(None, None, (3, 4)))

    #: Whether or not the visible image cache is valid
    _visible_cache_valid = Bool

    #: The cached image.
    _cached_visible_image = ArrayOrNone(shape=(None, None, (3, 4)))

    #: The cached destination rectangle.
    _cached_rect = Tuple(Float, Float, Float, Float)

    def rescale(self, scale, center=None):
        """ Rescale the image relative to a central point.

        Parameters
        ----------
        scale : float
            The new scale factor for the component.
        center : tuple of x, y
            The fixed point of the zoom in component coordinates.  If not
            supplied, then the center of the component will be used.
        """
        if center is None:
            center = np.array([self.x2, self.y2])/2.0
        else:
            center = np.array(center)

        # shift center into top-left based coordinates
        origin = np.array([self.x, self.y2])
        center = center - origin

        # scale offset relative to center point
        old_scale = self.scale
        offset = np.array(self.offset)
        new_offset = tuple(scale * (offset - center)/old_scale) + center

        # change scale and offset
        self.offset = tuple(new_offset.tolist())
        self.scale = scale

    # ------------------------------------------------------------------------
    # Component interface
    # ------------------------------------------------------------------------

    def _draw_mainlayer(self, gc, view_bounds=None, mode="normal"):
        """ Draws the image. """
        if not self._cache_valid:
            self._compute_cached_image()
        if not self._visible_cache_valid:
            self._compute_visible_image()
        if self._cached_visible_image is not None:
            gc.draw_image(self._cached_visible_image, self._cached_rect)

    # ------------------------------------------------------------------------
    # Object interface
    # ------------------------------------------------------------------------

    def __init__(self, image_data, **traits):
        traits['image_data'] = image_data
        super().__init__(**traits)

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _compute_cached_image(self):
        """ Extract the raw bytes to display, mapping colors if needed """
        if self.image_data is None:
            self._cached_image = None
            self._cache_valid = True
            return

        if self.image_data.color_space is None and self.color_map is not None:
            low, high = self.image_data.range
            self.color_map.range.low_setting = low
            self.color_map.range.high_setting = high

        self._cached_image = self.image_data.to_rgb(self.color_map.map_screen)
        self._cache_valid = True
        self._visible_cache_valid = False

    def _compute_visible_image(self):
        """ Clip the image data to just what is visible.

        Returns
        -------
        image, rectangle : array, 4-tuple
            The visible slice of the image, together with the rectangle in
            screen-space where the image is actually displayed (may be less
            than the full extent of the component).

        Notes
        -----

        This routine needs to handle the fact that images are assumed to be
        indexed with row 0 at the top (raster coordinates) where Kiva/Enable
        have a coordinate system with origin at the bottom left (mathematical
        coordinates).  Additionally we need to decide how we want to handle
        resizing of the component: as the window grows or shrinks, there is
        some fixed point in the rendererd image, which by default in Enable
        is the bottom-left corner.  This feels unnatural for images, and so
        we would prefer to keep the top-left corner as the origin.

        The computational strategy is then:
            * convert component corners to coordinates relative to origin.
            * apply scale and offset
            * snap to integer pixel coordinates and clip so adjusted cordinates
              give valid row and column indices
            * slice out the visible region (or return nothing if empty)
            * apply inverse scale and offset to array slice coordinates
            * convert back to usual Kiva coordinates
        """
        if self._cached_image is None:
            # nothing to see here
            return None, (0, 0, 0, 0)

        # handle slicing the plane of interest out of the image
        image = self._cached_image
        if image.ndim == 5:
            image = image[self.time_slice]
        if image.ndim >= 4:
            image = image[self.plane_slice]

        # origin is top-left, get corners relative to fixed point
        origin = np.array([self.x, self.y2])
        bottom_left = np.array([self.x, self.y]) - origin
        top_right = np.array([self.x2, self.y2]) - origin

        scale = self.scale
        offset = np.array(self.offset)
        # add 1 to shape because bounds are measured at pixel edges
        bounds = np.array(image.shape[1::-1]) + 1

        # apply scale and offset, widening to pixel boundaries
        c1, r1 = bottom_left = np.clip(np.floor(
            (bottom_left - offset)/scale), 0, bounds).astype(int)
        c2, r2 = top_right = np.clip(np.ceil(
            (top_right - offset)/scale), 0, bounds).astype(int)

        if c1 >= c2 or r1 >= r2:
            # nothing to show
            return None, (0, 0, 0, 0)

        # turn row and column corner values into slice
        n_rows = bounds[-1]
        image = image[(n_rows - r2):(n_rows - r1), c1:c2].copy()

        # apply inverse transformation
        bottom_left = bottom_left*scale + offset + origin
        top_right = top_right*scale + offset + origin
        rect = np.concatenate([bottom_left, top_right-bottom_left])

        self._cached_visible_image = image
        self._cached_rect = tuple(rect)
        self._visible_cache_valid = True

    # Trait change handlers --------------------------------------------------

    def _image_data_changed(self):
        """ When the data changes, make sure that offsets are still sane. """
        if self.image_data is None:
            return
        offset = np.array(self.offset)
        bounds = -self.scale * (np.array(self.image_data.size[:-3:-1]) + 1)
        if ((0 > offset) | (offset > bounds)).any():
            self.offset = (0, bounds[1])

    @on_trait_change('+invalidate_cache')
    def _invalidate_cache(self):
        self._cache_valid = False
        self.invalidate_and_redraw()

    @on_trait_change('bounds,+invalidate_visible_cache')
    def _invalidate_visible_cache(self):
        self._visible_cache_valid = False
        self.request_redraw()
