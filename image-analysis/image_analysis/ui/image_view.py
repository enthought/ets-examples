# -*- coding: utf-8 -*-
"""
Model object representing an image which can be manipulated.
"""
from __future__ import absolute_import, division, print_function

from chaco.api import DataRange1D, color_map_functions, color_map_name_dict
from enable.api import Component, ComponentEditor
from traits.api import Enum, Instance, List, Str, on_trait_change
from traitsui.api import HGroup, Item, ModelView, RangeEditor, TextEditor, UItem, View

from image_analysis.model.image import Image
from .components.image_data_component import ImageDataComponent
from .tools.offset_drag_tool import OffsetDragTool


image_view = View(
    UItem(
        'component',
        editor=ComponentEditor()
    ),
    HGroup(
        Item(
            'model.image_data.size',
            editor=TextEditor(format_func=lambda x: u'{}×{}'.format(*x)),
            show_label=False,
            style='readonly',
        ),
        Item(
            'color_map_name',
            label='Color Map:',
            enabled_when='model.image_data.color_space is None',
        ),
        Item(
            'object.component.scale',
            label='Zoom:',
            editor=RangeEditor(low=0.125, high=8.0)
        ),
    ),
    resizable=True,
)


class ImageView(ModelView):
    """ ModelView for an Image

    The actual image is displayed in a custom Enable component.
    """

    #: The image model being edited.
    model = Instance(Image)

    #: The image plot to display.
    component = Instance(Component)

    #: The color map to use for the display.
    color_map_name = Enum('viridis', values='color_map_names')

    #: All the known color map names.
    color_map_names = List(Str)

    #: TraitsUI View
    traits_view = image_view

    # ------------------------------------------------------------------------
    # Handler interface
    # ------------------------------------------------------------------------

    def init(self, ui_info):
        ui_info.ui.title = self.model.name

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    # Trait change handlers --------------------------------------------------

    @on_trait_change('model.image_data')
    def _image_data_updated(self):
        self.component.image_data = self.model.image_data

    @on_trait_change('color_map_name')
    def _color_map_updated(self):
        self.component.color_map = color_map_name_dict[self.color_map_name](
            range=DataRange1D())

    # Trait defaults ---------------------------------------------------------

    def _component_default(self):
        color_map = color_map_name_dict[self.color_map_name](
            range=DataRange1D())
        component = ImageDataComponent(
            self.model.image_data, color_map=color_map)
        drag_tool = OffsetDragTool(component=component)
        component.tools.append(drag_tool)
        return component

    def _color_map_names_default(self):
        return [f.__name__ for f in color_map_functions]
