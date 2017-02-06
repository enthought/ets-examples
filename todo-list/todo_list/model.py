"""
To-Do List Model Classes
========================

This module provides two classes that together provide the business logic for
a simple to-do list application.
"""

from __future__ import absolute_import, print_function, unicode_literals

from traits.api import (
    Bool, HasStrictTraits, Instance, Int, List, Property, Str, on_trait_change)


class ToDoItem(HasStrictTraits):
    """ A task in a to-do list.

    A to-do item has a description and a completed flag as its state.
    """

    #: The description of the task.
    description = Str

    #: Whether or no the task has been completed.
    completed = Bool


class ToDoList(HasStrictTraits):
    """ A list of tasks that need to be done.

    This provides a list of :py:class:`ToDoItem` instances, as well as a list
    of the remaining items and the count of the remaining items.

    Notes
    -----
    This demonstrates both using :py:func:`on_trait_change` and Traits
    :py:class:`Property` handlers to handle re-computation based on updates
    for pedagogical reasons.
    """

    #: The list of tasks that we want to perform.
    items = List(Instance(ToDoItem, ()))

    #: The list of items that still need to be completed.
    remaining_items = List(Instance(ToDoItem))

    #: The number of remaining items.
    remaining = Property(Int, depends_on='remaining_items')

    # Trait handlers ---------------------------------------------------------

    @on_trait_change('items.completed')
    def update(self):
        self.remaining_items = [item for item in self.items
                                if not item.completed]

    def _get_remaining(self):
       return len(self.remaining_items)
