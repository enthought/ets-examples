
from future.builtins import super

from traits.api import Callable, HasTraits, Instance, Str, Type, provides

from .array_image_data import ArrayImageData
from .i_color_space import IColorSpace
from .i_operation import IOperation
from .i_parameters import IParameters


def is_greyscale(image_data):
    """ Return true image data does not have color channels """
    return image_data.color_space is None


@provides(IOperation)
class SimpleOperation(HasTraits):
    """ A basic single-input function. """

    #: The human-friendly name of the operation.
    name = Str

    #: The function to apply to the bytes of the image data
    function = Callable

    #: The type of parameters to use.
    parameters = Type(IParameters)

    #: The output color space, or None if color space should match input.
    color_space = Instance(IColorSpace)

    #: A callable that returns whether the image_data matches what is needed.
    is_available = Callable(lambda image_data: True)

    def __init__(self, function, **traits):
        traits.setdefault('name', function.__name__)
        traits['function'] = function
        super().__init__(**traits)

    def __call__(self, image_data, parameters):
        if parameters is not None:
            args, kwargs = parameters.to_function_args()
        else:
            args = ()
            kwargs = {}
        data = self.function(image_data.data, *args, **kwargs)
        if self.color_space is None:
            color_space = image_data.color_space
        else:
            color_space = self.color_space
        return ArrayImageData(data=data, color_space=color_space)

    def to_script(self, image_name, parameters):
        if parameters is not None:
            args, kwargs = parameters.to_function_args()
        else:
            args = ()
            kwargs = {}
        args = ''.join((', ' + repr(arg)) for arg in args)
        kwargs = ''.join(', {}={}'.format(key, repr(value))
                         for key, value in kwargs.items())
        return "{}({}{}{})".format(
            self.function.__name__, image_name, args, kwargs)
