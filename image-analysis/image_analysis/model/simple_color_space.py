"""
Simple colorspace implementations using scikits image converters.
"""
from __future__ import absolute_import, division, print_function

from skimage.color import convert_colorspace
from traits.api import HasStrictTraits, List, Str, provides

from .i_color_space import IColorSpace


@provides(IColorSpace)
class SimpleColorSpace(HasStrictTraits):
    """ Standard colorspaces that scikits image understands. """

    #: The name of the color space in scikits image.
    name = Str('hsv')

    #: The names of the channels.
    channel_names = List(Str)

    #: The number of channels.
    n_channels = 3

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
        return convert_colorspace(data, self.name, 'rgb')

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
        return convert_colorspace(rgb_data, 'rgb', self.name)


# standard color space instances
hsv_color_space = SimpleColorSpace(
    name='hsv',
    channel_names=['hue', 'saturation', 'value']
)

rgb_cie_color_space = SimpleColorSpace(
    name='rgb cie',
    channel_names=['red', 'green', 'blue']
)

xyz_color_space = SimpleColorSpace(
    name='xyz',
    channel_names=['x', 'y', 'z']
)

yuv_color_space = SimpleColorSpace(
    name='yuv',
    channel_names=['luminance', 'chrominance_blue', 'chrominance_red'],
)

yiq_color_space = SimpleColorSpace(
    name='yiq',
    channel_names=['luminance', 'in_phase', 'quadrature'],
)

ypbpr_color_space = SimpleColorSpace(
    name='ypbpr',
    channel_names=['luminance', 'chrominance_blue', 'chrominance_red'],
)

ycbcr_color_space = SimpleColorSpace(
    name='ycbcr',
    channel_names=['luminance', 'chrominance_blue', 'chrominance_red'],
)
