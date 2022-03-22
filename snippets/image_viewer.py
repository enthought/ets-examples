# Copyright (c) 2005-2022, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
Image Preview Application
=========================

This example shows a very basic image preview application using the TraitsUI
FileEditor and ImageEditor.  Some basic image editing and filtering is provided
via NumPy and Scikit Image.

Key things this example demonstrates:

* The use of the ``Image`` trait and the ``ImageEditor`` with a changing
  ``ArrayImage``.
* Separation of concerns in the Model and ModelView.
* The use of Actions and Groups to build structured toolbars and menubars.
* The use of ``id`` to remember user layout preferences.
"""

import numpy as np
from skimage import img_as_float, img_as_ubyte
from skimage.io import imread
from skimage.restoration import denoise_nl_means, estimate_sigma

from pyface.api import Image, ArrayImage
from pyface.array_image import ImageArray
from traits.api import File, HasStrictTraits, Instance, observe
from traitsui.api import (
    Action, ActionGroup, FileEditor, HSplit, ImageEditor, Item, Menu, MenuBar,
    ModelView, ToolBar, View
)


#: A transparent, 256x256 RGBA image array.  This is used when no other image
#: is available.
blank_image = np.zeros((256, 256, 4), dtype='uint8')


class ImageModel(HasStrictTraits):
    """A model object holding an image stored in an array.

    This has methods for basic transformation of the image, as well as an
    example of a more complex denoising filter using scikits image.
    """

    #: The path to the image file.
    image_path = File('~')

    #: The RGB(A) bytes of the image
    data = ImageArray()

    def load_image(self):
        try:
            self.data = imread(self.image_path)
        except Exception:
            self.data = blank_image

    def rotate(self, direction):
        """Rotate the image clockwise or anticlockwise."""
        if direction == "clockwise":
            self.data = np.rot90(self.data, axes=(1, 0))
        else:
            self.data = np.rot90(self.data, axes=(0, 1))

    def flip(self, direction):
        """Flip the image horizontally or vertically."""
        if direction == "vertical":
            self.data = np.flipud(self.data)
        else:
            self.data = np.fliplr(self.data)

    def denoise(self):
        """Do denoising with scikit image."""
        data = img_as_float(self.data)
        sigma_est = np.mean(estimate_sigma(data, channel_axis=-1))
        new_data = denoise_nl_means(
            data,
            h=0.8 * sigma_est,
            sigma=sigma_est,
            fast_mode=True,
            patch_size=5,
            patch_distance=6,
            channel_axis=-1,
        )
        self.data = img_as_ubyte(new_data)

    @observe('image_path')
    def _update_image(self, event):
        self.load_image()

    def _data_default(self):
        return blank_image


class ImageView(ModelView):
    """A model view of an image with actions.
    """

    #: The image model being viewed.
    model = Instance(ImageModel, (), allow_none=False)

    #: The image to display.
    image = Image()

    def rotate_left(self):
        """Rotate the image anticlockwise."""
        self.model.rotate("anticlockwise")

    def rotate_right(self):
        """Rotate the image clockwise."""
        self.model.rotate("clockwise")

    def flip_horizontal(self):
        """Flip the image horizontally."""
        self.model.flip("horizontal")

    def flip_vertical(self):
        """Flip the image vertically."""
        self.model.flip("vertical")

    def reload(self):
        """Reload the image from disk."""
        self.model.load_image()

    @observe('model.data')
    def _update_image(self, event):
        self.image = ArrayImage(data=self.model.data)

    def _image_default(self):
        return ArrayImage(data=self.model.data)

    view = View(
        HSplit(
            Item(
                'model.image_path',
                editor=FileEditor(
                    dialog_style='open',
                    filter=["*.png", "*.jpg", "*.jpeg"]
                ),
                style='custom',
            ),
            Item(
                'image',
                editor=ImageEditor(
                    scale=True,
                    preserve_aspect_ratio=True,
                    allow_upscaling=True,
                ),
                springy=True,
                resizable=True,
            ),
            show_labels=False,
            # NOTE: this id means the position of the sash will be saved
            id='viewer_split'
        ),
        resizable=True,
        toolbar=ToolBar(
            ActionGroup(
                Action(
                    name="Rotate Left",
                    tooltip="Rotate Left",
                    action='rotate_left',
                    image='rotate_left',
                ),
                Action(
                    name="Rotate Right",
                    tooltip="Rotate Right",
                    action='rotate_right',
                    image='rotate_right',
                ),
                Action(
                    name="Flip Horizontally",
                    tooltip="Flip Horizontally",
                    action='flip_horizontal',
                    image='flip_horizontal',
                ),
                Action(
                    name="Flip Vertically",
                    tooltip="Flip Vertically",
                    action='flip_vertical',
                    image='flip_vertical',
                ),
                name="Transpose Group",
                id="transpose_group",
            ),
            ActionGroup(
                Action(
                    name="Denoise",
                    tooltip="Denoise",
                    action='denoise',
                    image='denoise',
                ),
                name="Filter Group",
                id="filter_group",
            ),
            image_size=(24, 24),
            show_tool_names=False,
        ),
        menubar=MenuBar(
            Menu(
                Action(name="Revert Image", action="revert"),
                name="File",
                id="file_menu",
            ),
            Menu(
                ActionGroup(
                    Action(name="Rotate Left", action='rotate_left'),
                    Action(name="Rotate Right", action='rotate_right'),
                    Action(name="Flip Horizontally", action='flip_horizontal'),
                    Action(name="Flip Vertically", action='flip_vertical'),
                    name="Transpose Group",
                    id="transpose_group",
                ),
                ActionGroup(
                    Action(name="Denoise", action='denoise'),
                    name="Filter Group",
                    id="filter_group",
                ),
                name="Edit",
                id="edit_menu",
            ),
        ),
        # NOTE: this id means the size of the window will be saved
        id='image_preview',
    )


if __name__ == '__main__':
    view = ImageView()
    view.configure_traits()
