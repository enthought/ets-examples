"""
Interface for color spaces.
"""
from __future__ import absolute_import, division, print_function

from traits.api import Range, Interface, List, Str


class IColorSpace(Interface):
    """ Interface for color spaces. """

    #: The name of the color space.
    name = Str

    #: The names of the channels.
    channel_names = List(Str)

    #: The number of channels.
    n_channels = Range(low=1)

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
        raise NotImplementedError()

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
        raise NotImplementedError()
