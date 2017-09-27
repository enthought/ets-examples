from traits.api import Str, Trait

from image_analysis.image_data_transforms import flip
from .image_command import DataCommand


class FlipImage(DataCommand):

    source = Str

    destination = Str

    axis = Trait('horizontal', {
        'horizontal': -1,
        'vertical': -2,
        'plane': -3,
        'time': -4
    })

    def _do(self):
        source_image = self.data.images[self.source]
        result = flip(source_image, self.axis_)
        self.data[self.destination] = result

    def _source_default(self):
        return self.data.active_image_name

    def _destination_default(self):
        return self.source
