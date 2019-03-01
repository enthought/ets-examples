# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
This module provides the UI classes that provide the UI logic and views for
a simple to-do list application.  This is a fairly simple UI, with each item
displayed in a list editor, and a toggle to allow the user to switch between
seeing all items or just the remaining items.  This also shows a basic action
which is available as a menu item and a button.
"""

from __future__ import absolute_import, print_function, unicode_literals

import os

from traits.api import (
    Button, Enum, Instance, List, Property, Str, on_trait_change)
from traitsui.api import (
    ButtonEditor, Controller, HGroup, InstanceEditor, Item, ListEditor,
    ModelView, Spring, VGroup, View)
from traitsui.menu import Action, ActionGroup, Menu, MenuBar

from .model import ToDoItem, ToDoList


# ----------------------------------------------------------------------------
# TraitsUI Actions and Menus
# ----------------------------------------------------------------------------

new_item_action = Action(
    name='New Item',
    action='new_item',
    accelerator='Ctrl++'
)

menubar = MenuBar(
    Menu(
        ActionGroup(new_item_action, name='list_group'),
        name='Edit',
    ),
)


# ----------------------------------------------------------------------------
# TraitsUI Views
# ----------------------------------------------------------------------------

#: Stripped down view for use in list editor
to_do_item_view = View(
    HGroup(
        Item('completed', show_label=False),
        Item('description', show_label=False, springy=True),
        Item('controller.delete',show_label=False)
    ),
)


#: View for main model view
todo_list_view = View(
    VGroup(
        HGroup(
            Item(
                'remaining',
                style='readonly',
                show_label=False
            ),
            Spring(),
            Item('display_selection', label='Show:'),
        ),
        Item(
            'displayed_items',
            show_label=False,
            style='readonly',
            springy=True,
            editor=ListEditor(
                style='custom',
                editor=InstanceEditor(view=to_do_item_view),
            ),
        ),
    ),
    title="To Do List",
    buttons=[new_item_action],
    menubar=menubar,
    resizable=True,
    width=480,
    height=640,
)


# ----------------------------------------------------------------------------
# TraitsUI Handlers
# ----------------------------------------------------------------------------

class ToDoItemController(Controller):
    """ A controller for list items in the view

    We need this to add a 'delete' button to the view, which we can't do
    from the item by itself.
    """

    #: The item being displayed
    model = Instance(ToDoItem)

    #: The todo list being displayed in the larger view
    todo_list = Instance(ToDoList)

    #: A button to trigger removal.
    delete = Button

    # Trait handlers ---------------------------------------------------------

    def _delete_changed(self):
        self.todo_list.items.remove(self.model)


class ToDoListModelView(ModelView):
    """ A ModelView for the ToDoList

    This ModelView allows the user to switch the view between the list of all
    items and the list of remaining items, as well as add new items.
    """

    #: The todo list that we are using as the model.
    model = Instance(ToDoList)

    #: Whether we want to see all items, or just the remaining items.
    display_selection = Enum('all', 'remaining')

    #: The list of items that we are actually viewing.
    displayed_items = List(Instance(ToDoItemController))

    #: A human-friendly string reporting the number of items remaining
    remaining = Property(Str, depends_on='model.remaining')

    # Action handlers --------------------------------------------------------

    def new_item(self, ui_info):
        """ Handle an "New Item" action.

        This simply adds a new, empty item to the model's items.
        """
        new_item = ToDoItem()
        self.model.items.append(new_item)

    # Trait handlers ---------------------------------------------------------

    @on_trait_change('model.items.completed,display_selection')
    def _update_displayed_items(self):
        # handle situation where model may be None temporarily
        if self.model is None:
            return []

        if self.display_selection == 'all':
            items = self.model.items
        else:
            items = self.model.remaining_items

        self.displayed_items = [
            ToDoItemController(model=item, todo_list=self.model)
            for item in items]

    def _get_remaining(self):
        remaining = self.model.remaining
        if remaining == 0:
            return 'No items remaining'
        elif remaining == 1:
            return '1 item remaining'
        else:
            return '{} items remaining'.format(remaining)

    # Default TraitsUI view --------------------------------------------------

    traits_view = todo_list_view
