
from traits.api import Interface, Str, Type

from .i_parameters import IParameters


class IOperation(Interface):

    #: The human-friendly name of the operation.
    name = Str

    #: The type of parameters to use.
    parameters = Type(IParameters)

    def is_available(self, image_data):
        """ Can the operation be used on this image data? """
        raise NotImplementedError()

    def __call__(self, image_data, parameters):
        raise NotImplementedError()

    def to_script(self, image_name, parameters):
        raise NotImplementedError()
