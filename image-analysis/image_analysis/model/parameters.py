from future.builtins import super

from skimage import img_as_bool

from traits.api import Either, Enum, Float, Instance

from .base_parameters import BaseParameters
from .i_image_data import IImageData


class MaskParameters(BaseParameters):

    #: A mask image_data to restrict an operation
    mask = Instance(IImageData)

    def to_function_args(self):
        """ Convert the parameters to positional and keyword arguments.

        By default this constructs kword arguments out of all traits where the
        'parameter' metadata is True.

        Returns
        -------
        args : tuple
            The positional arguments of the parameters, always empty for
            default.
        kwargs : dict
            The keyword arguments of the parameters.
        """
        args, kwargs = super().to_function_args()
        if self.mask is not None:
            kwargs['mask'] = img_as_bool(self.mask.data)
        return (), kwargs


class GaborParameters(BaseParameters):

    #: The frequency in pixels.
    frequency = Float(parameter=True)

    #: The orientation in radians.
    theta = Float(0.0, parameter=True)

    #: The bandwidth captured by the filter.
    bandwidth = Float(1.0, parameter=True)

    #: The standard deviation in the x direction (before rotation).
    sigma_x = Either(None, Float, parameter=True)

    #: The standard deviation in the y direction (before rotation).
    sigma_x = Either(None, Float, parameter=True)

    #: The size of the kernel in number of standard deviations.
    n_stds = Float(3.0, parameter=True)

    #: The phase offset of the harmonic function, in radians.
    offset = Float(parameter=True)

    #: The convolution mode.
    mode = Enum('reflect', 'constant', 'nearest', 'mirror', 'wrap',
                parameter=True)

    #: The value to fill past edges.
    n_stds = Float(3.0, parameter=True)
