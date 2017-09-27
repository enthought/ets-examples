"""
Basic ImageData class which stores image data in an array
"""
from __future__ import absolute_import, division, print_function

import numpy as np
from skimage import img_as_ubyte
from skimage.color import gray2rgb

from traits.api import (
    Array, ArrayOrNone, HasStrictTraits, Instance, Property, Tuple,
    cached_property, provides
)

from .i_color_space import IColorSpace
from .i_image_data import IImageData
from .rgb_color_space import rgb_color_space, rgba_color_space
from .model_traits import Size


@provides(IImageData)
class ArrayImageData(HasStrictTraits):
    """ Image data and information about the image data's structure.

    ArrayImageData instances are intended to be immutable.  Once created, data
    should not be modified, but rather a new instance created.
    """

    #: An array holding the data.
    data = Array(allow_none=False)

    #: The number of dimensions (excluding color channels)
    n_dim = Property(depends_on=['array', 'color_space'])

    #: The numerical type of the channels.
    type = Property(depends_on='array')

    #: The the color space being used, or None if greyscale or labels.
    color_space = Instance(IColorSpace)

    #: The minimum and maximum values in each channel.
    range = Property(Tuple, depends_on='array')

    #: The size of the image.
    size = Property(Size, depends_on='array')

    #: A cache of an rgb(a) version of the image for speed.
    _rgb_data = ArrayOrNone

    # ------------------------------------------------------------------------
    # IImageData interface
    # ------------------------------------------------------------------------

    def to_rgb(self, color_map=None):
        """ The data as an rgb24 or rgba32 array, suitable for viewers.

        Parameters
        ----------
        color_map : callable
            An optional color_map to apply to greyscale data.  If this is not
            supplied then greyscale data will be converted with .

        Returns
        -------
        rgb_data : array of shape (n, m, 3 or 4)
            An array of rgba or rgb data.
        """
        if self.color_space is not None:
            if self._rgb_data is None:
                self._rgb_data = img_as_ubyte(
                    self.color_space.to_rgb(self.data))
            return self._rgb_data
        elif color_map is None:
            if self._rgb_data is None:
                self._rgb_data = img_as_ubyte(gray2rgb(self.data))
            return self._rgb_data
        else:
            return img_as_ubyte(color_map(self.data))

    # ------------------------------------------------------------------------
    # object interface
    # ------------------------------------------------------------------------

    def __init__(self, data, **traits):
        traits['data'] = data
        super(ArrayImageData, self).__init__(**traits)

    # ------------------------------------------------------------------------
    # private interface
    # ------------------------------------------------------------------------

    def _color_space_default(self):
        if len(self.data.shape) >= 3:
            if self.data.shape[-1] == 3:
                return rgb_color_space
            elif self.data.shape[-1] == 4:
                return rgba_color_space
        return None

    # trait property handlers ------------------------------------------------

    @cached_property
    def _get_n_dim(self):
        if self.color_space is not None:
            return self.data.ndim - 1
        return self.data.ndim

    @cached_property
    def _get_type(self):
        return self.data.dtype.type

    @cached_property
    def _get_size(self):
        return self.data.shape[:self.n_dim]

    @cached_property
    def _get_range(self):
        shape = self.data.shape[self.n_dim:]
        if issubclass(self.type, np.floating):
            if np.any(self.data < 0):
                return (
                    np.full(shape, -1.0, dtype=self.type),
                    np.ones(shape=shape, dtype=self.type)
                )
            else:
                return (
                    np.zeros(shape=shape, dtype=self.type),
                    np.ones(shape=shape, dtype=self.type)
                )
        elif issubclass(self.type, np.integer):
            return (
                np.full(shape, np.iinfo(self.type).min, dtype=self.type),
                np.full(shape, np.iinfo(self.type).max, dtype=self.type)
            )
