

from apptools.undo.api import AbstractCommand
from traits.api import Instance

from .i_image_data import IImageData
from .i_operation import IOperation
from .i_parameters import IParameters
from .image import Image


class ImageCommand(AbstractCommand):

    data = Instance(Image)

    operation = Instance(IOperation)

    parameters = Instance(IParameters)

    _before = Instance(IImageData)

    _after = Instance(IImageData)

    def do(self):
        self._before = self.data.image_data
        self._after = self.operation(self.data.image_data, self.parameters)
        self.redo()

    def undo(self):
        self.image.image_data = self._before

    def redo(self):
        self.image.image_data = self._after
