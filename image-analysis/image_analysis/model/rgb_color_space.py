"""
RGB color spaces.
"""
from __future__ import absolute_import, division, print_function

import numpy as np
from traits.api import HasStrictTraits, Int, List, Str, provides

from .i_color_space import IColorSpace


@provides(IColorSpace)
class RgbColorSpace(HasStrictTraits):
    """ RGB and RGBA color spaces. """

    #: The name of the color space in scikits image.
    name = Str('rgb')

    #: The names of the channels.
    channel_names = List(Str)

    #: The number of channels.
    n_channels = Int(3)

    def to_rgb(self, data):
        """ Convert an array in this color space to rgb or rgba.

        Parameters
        ----------
        data : array
            A numpy array of the appropriate type.

        Returns
        -------
        rgb_data : array of rgb or rgba data
            An array of rgb or rgba data.
        """
        return data

    def from_rgb(self, rgb_data):
        """ Convert an rgb array to this color space.

        Parameters
        ----------
        rgb_data : array of rgb or rgba data
            An array of rgb or rgba data.

        Returns
        -------
        array : array
            A numpy array of the appropriate type.
        """
        if rgb_data.shape[-1] > self.n_channels:
            # discard alpha channel
            return rgb_data[..., :-1]
        elif rgb_data.shape[-1] > self.n_channels:
            # add opaque alpha channel
            shape = rgb_data.shape[:-1]+(self.n_channels,)
            data = np.empty(shape=shape, dtype=rgb_data.dtype)
            data[..., :rgb_data.shape[-1]] = rgb_data
            if isinstance(rgb_data.dtype.type, np.floating):
                data[..., -1] = 1.0
            else:
                data[..., -1] = np.iinfo(rgb_data.dtype.type).max
            return data
        else:
            return rgb_data


# standard rgb space instances
rgb_color_space = RgbColorSpace(
    name='rgb',
    channel_names=['red', 'green', 'blue']
)

rgba_color_space = RgbColorSpace(
    name='rgba',
    channel_names=['red', 'green', 'blue', 'alpha'],
    n_channels=4
)
