"""
Interface for objects which provide image data.
"""
from __future__ import absolute_import, division, print_function

from traits.api import Any, Array, Enum, Instance, Interface, Tuple

from .i_color_space import IColorSpace
from .model_traits import Size


class IImageData(Interface):
    """ Image data and information about the image data's structure.

    Image data instances always have a data attribute (possibly a Property)
    which holds an array of the data suitable for use with scikits-image,
    and so in particular, compatible with that library's assumptions.

    IImageData instances are intended to be immutable.  Once created, data
    should not be modified, but rather a new instance created.
    """

    #: An array holding the data.
    data = Array(allow_none=False)

    #: The number of dimensions (excluding color channels)
    n_dim = Enum(2, 3, 4)

    #: The dtype of the channels.
    type = Any

    #: The the color space being used, or None if greyscale or labels.
    color_space = Instance(IColorSpace)

    #: The minimum and maximum values in each channel.
    range = Tuple

    #: The size of the image.
    size = Size

    def to_rgb(self, color_map=None):
        """ The data as an rgb24 or rgba32 array, suitable for viewers.

        Parameters
        ----------
        color_map : AbstractColorMap instance
            An optional color_map to apply to the data.  Implementers of this
            method should do something sensible with a color_map value of None.

        Returns
        -------
        rgb_data : array of uint8 of shape (n, m, 3 or 4)
            An array of rgba data.
        """
        raise NotImplementedError()

    def thumbnail(self, size=(16, 16)):
        """ Create a thumbnail image of the data for display with in a UI.

        This will create a thumbnail of the desired size, ensuring that the
        entire image is visible, maintaing aspect ratio, and filling empty
        space with transparent values.

        Parameters
        ----------
        size : tuple of int, int
            The width and height of the thumbnail.

        Returns
        -------
        thumbnail_data : array of uint8 of shape (w, h, 4)
            The thumbnail data as an rgba array.
        """
        raise NotImplementedError()
