# -*- coding: utf-8 -*-
"""
Model object representing an image which can be manipulated.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from apptools.undo.api import CommandStack
from chaco.api import DataRange1D, color_map_functions, color_map_name_dict
from enable.api import Component, ComponentEditor
from traits.api import Instance, List, Unicode, on_trait_change
from traitsui.api import (
    EnumEditor, HGroup, Item, ModelView, TextEditor, UItem, View
)

from image_analysis.model.image_namespace import ImageNamespace
from .components.image_data_component import ImageDataComponent
from .tools.offset_drag_tool import OffsetDragTool
from .tools.scale_zoom_tool import ScaleZoomTool


image_view = View(
    UItem(
        'component',
        editor=ComponentEditor()
    ),
    HGroup(
        Item(
            'name', editor=EnumEditor(name='names')
        ),
        Item(
            'object.component.image_data.size',
            editor=TextEditor(format_func=lambda x: u'{}×{}'.format(*x)),
            show_label=False,
            style='readonly',
        ),
        Item(
            'color_map_name',
            label='Color Map:',
            enabled_when='object.component.image_data.color_space is None',
            editor=EnumEditor(name='color_map_names')
        ),
        Item(
            'scale',
            label='Zoom:',
        ),
    ),
    resizable=True,
)


class ImageView(ModelView):
    """ ModelView for an Image

    The actual image is displayed in a custom Enable component.
    """

    #: The image model being edited.
    model = Instance(ImageNamespace)

    #: The name of the image being edited.
    name = Unicode

    #: The list of image names.
    names = List(Unicode)

    #: The image plot to display.
    component = Instance(Component)

    #: The zoom tool used by the component.
    zoom_tool = Instance(ScaleZoomTool)

    #: The color map to use for the display.
    color_map_name = Unicode('viridis')

    #: All the known color map names.
    color_map_names = List(Unicode)

    #: The scale as a more user-friendly string.
    scale = Unicode

    command_stack = Instance(CommandStack, ())

    #: Default TraitsUI View
    traits_view = image_view

    # ------------------------------------------------------------------------
    # Handler interface
    # ------------------------------------------------------------------------

    def init(self, ui_info):
        ui_info.ui.title = self.name
        self.scale = u"{:.1%}".format(self.component.scale)

    def object_scale_changed(self, ui_info):
        try:
            self.component.scale = float(self.scale.replace('%', ''))/100.0
        except ValueError:
            pass

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    # Trait change handlers --------------------------------------------------

    @on_trait_change('name')
    def _name_updated(self):
        self.component.image_data = self.model.images[self.name]

    @on_trait_change('model:images_items')
    def _images_updated(self, event):
        self.names = sorted(self.model.images)
        if self.name in event.removed:
            self.name = self.model.images.active_image

    @on_trait_change('color_map_name')
    def _color_map_name_updated(self):
        self.component.color_map = color_map_name_dict[self.color_map_name](
            range=DataRange1D())

    @on_trait_change('component.scale')
    def _component_scale_updated(self):
        self.scale = u"{:.1%}".format(self.component.scale)

    # Trait defaults ---------------------------------------------------------

    def _component_default(self):
        color_map = color_map_name_dict[self.color_map_name](
            range=DataRange1D())
        component = ImageDataComponent(
            self.model.images[self.name], color_map=color_map)
        drag_tool = OffsetDragTool(component=component)
        component.tools.append(drag_tool)
        self.zoom_tool = ScaleZoomTool(component=component)
        component.tools.append(self.zoom_tool)
        return component

    def _color_map_names_default(self):
        return sorted([unicode(f.__name__) for f in color_map_functions])

    def _name_default(self):
        return self.model.active_image

    def _names_default(self):
        return sorted(self.model.images)
