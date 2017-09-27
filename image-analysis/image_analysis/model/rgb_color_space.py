"""
RGB color spaces.
"""
from __future__ import absolute_import, division, print_function

import numpy as np
from traits.api import HasStrictTraits, ReadOnly, provides

from .i_color_space import IColorSpace


@provides(IColorSpace)
class RGBColorSpace(HasStrictTraits):
    """ RGB and RGBA color spaces. """

    #: The name of the color space in scikits image.
    name = ReadOnly

    #: The names of the channels.
    channel_names = ReadOnly

    #: The number of channels.
    n_channels = ReadOnly

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
        if rgb_data.shape[-1] not in {3, 4}:
            msg = "Expected last dimesnions of size 3 or 4, given {}"
            raise ValueError(msg.format(rgb_data.shape[-1]))

        if rgb_data.shape[-1] > self.n_channels:
            # discard alpha channel
            return rgb_data[..., :self.n_channels]
        elif rgb_data.shape[-1] < self.n_channels:
            # add opaque alpha channel
            n_channels = rgb_data.shape[-1]
            shape = rgb_data.shape[:-1]+(self.n_channels,)
            data = np.empty(shape=shape, dtype=rgb_data.dtype)
            data[..., :n_channels] = rgb_data
            if issubclass(rgb_data.dtype.type, np.floating):
                data[..., n_channels:] = 1.0
            else:
                data[..., n_channels:] = np.iinfo(rgb_data.dtype.type).max
            return data
        else:
            return rgb_data


# standard rgb space instances
rgb_color_space = RGBColorSpace(
    name='rgb',
    channel_names=('red', 'green', 'blue'),
    n_channels=3,
)

rgba_color_space = RGBColorSpace(
    name='rgba',
    channel_names=('red', 'green', 'blue', 'alpha'),
    n_channels=4,
)
