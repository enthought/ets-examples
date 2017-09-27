
from traits.api import Dict, HasStrictTraits, Instance, Property, Str

from .i_image_data import IImageData


class ImageNamespace(HasStrictTraits):
    """ A collection of images with associated names. """

    #: The mapping of names to image data.
    images = Dict(Str, Instance(IImageData))

    #: The name of the active image for operations.
    active_image_name = Str(None, allow_none=True)

    #: Tha active image's data
    active_image = Property(Instance(IImageData),
                            depends_on=['images', 'images_items',
                                        'active_image_name'])

    def get_data(self):
        return {
            'images': self.images,
            'active_image_name': self.active_image_name,
        }

    def set_data(self, data):
        images = data['images']
        active_image_name = data['active_image_name']
        # avoid active image not being in set of images for listeners
        if self.active_image_name in images:
            self.images = images
            self.active_image_name = active_image_name
        elif active_image_name in self.images:
            self.active_image_name = active_image_name
            self.images = images
        else:
            self.active_image_name = None
            self.images = images
            self.active_image_name = active_image_name

    def _get_active_image(self):
        if self.active_image_name is not None:
            return self.images.get(self.active_image_name)
        return None
