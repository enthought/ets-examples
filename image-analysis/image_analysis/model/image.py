"""
Model object representing an image which can be manipulated.
"""
from __future__ import absolute_import, division, print_function

from traits.api import Any, HasStrictTraits, Instance, Str

from .i_image_data import IImageData


class Image(HasStrictTraits):

    #: The human-readable name of the image.
    name = Str('Untitled')

    #: The (current) image data for the image.
    image_data = Instance(IImageData)

    #: The image metadata, if any.
    metadata = Any
