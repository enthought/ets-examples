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
Tests for To-do List View Code
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from unittest import TestCase

from traits.testing.unittest_tools import UnittestTools

from todo_list.model import ToDoItem, ToDoList
from todo_list.view import ToDoItemController, ToDoListModelView


class TestToDoItemModelView(TestCase, UnittestTools):

    def test_to_do_item_delete(self):
        # test that delete button works as expected
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do', completed=True)
        todo_list = ToDoList(items=[item_1, item_2])
        controller = ToDoItemController(model=item_1, todo_list=todo_list)

        with self.assertTraitChanges(todo_list, 'items_items', count=1):
            controller.delete = True

        self.assertEqual(todo_list.items, [item_2])


class TestToDoListModelView(TestCase, UnittestTools):

    def test_model_view(self):
        # test that handlers work statically
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do', completed=True)
        todo_list = ToDoList(items=[item_1, item_2])

        model_view = ToDoListModelView(model=todo_list)

        self.assertEqual(len(model_view.displayed_items), 2)
        self.assertEqual(
            [controller.model for controller in model_view.displayed_items],
            todo_list.items)
        self.assertEqual(model_view.remaining, '1 item remaining')

    def test_model_view_selection(self):
        # test that 'remaining' selection works
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do', completed=True)
        todo_list = ToDoList(items=[item_1, item_2])

        model_view = ToDoListModelView(
            model=todo_list, display_selection='remaining')

        self.assertEqual(len(model_view.displayed_items), 1)
        self.assertEqual(
            [controller.model for controller in model_view.displayed_items],
            todo_list.remaining_items)
        self.assertEqual(model_view.remaining, '1 item remaining')

    def test_model_view_selection_changed(self):
        # test that selection change works
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do', completed=True)
        todo_list = ToDoList(items=[item_1, item_2])

        model_view = ToDoListModelView(model=todo_list)

        with self.assertTraitChanges(model_view, 'displayed_items', count=1):
            model_view.display_selection = 'remaining'

        self.assertEqual(len(model_view.displayed_items), 1)
        self.assertEqual(
            [controller.model for controller in model_view.displayed_items],
            todo_list.remaining_items)
        self.assertEqual(model_view.remaining, '1 item remaining')

    def test_model_view_list_items_completed_changed(self):
        # test that changing 'completed' state works
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do')
        todo_list = ToDoList(items=[item_1, item_2])

        model_view = ToDoListModelView(
            model=todo_list, display_selection='remaining')

        with self.assertTraitChanges(model_view, 'displayed_items', count=1):
            item_2.completed = True

        self.assertEqual(len(model_view.displayed_items), 1)
        self.assertEqual(
            [controller.model for controller in model_view.displayed_items],
            todo_list.remaining_items)
        self.assertEqual(model_view.remaining, '1 item remaining')

    def test_model_view_list_items_changed(self):
        # test that changing list in place works
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do')
        todo_list = ToDoList(items=[item_1, item_2])

        model_view = ToDoListModelView(
            model=todo_list, display_selection='remaining')

        with self.assertTraitChanges(model_view, 'displayed_items', count=1):
            todo_list.items.remove(item_2)

        self.assertEqual(len(model_view.displayed_items), 1)
        self.assertEqual(
            [controller.model for controller in model_view.displayed_items],
            todo_list.remaining_items)
        self.assertEqual(model_view.remaining, '1 item remaining')

    def test_model_view_list_items_replaced(self):
        # test that changing entire list works
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do')
        todo_list = ToDoList(items=[item_1, item_2])

        model_view = ToDoListModelView(
            model=todo_list, display_selection='remaining')

        with self.assertTraitChanges(model_view, 'displayed_items', count=1):
            todo_list.items = [item_1]

        self.assertEqual(len(model_view.displayed_items), 1)
        self.assertEqual(
            [controller.model for controller in model_view.displayed_items],
            todo_list.remaining_items)
        self.assertEqual(model_view.remaining, '1 item remaining')

    def test_model_view_list_model_replaced(self):
        # test that changing model works
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do')
        todo_list = ToDoList(items=[item_1, item_2])

        model_view = ToDoListModelView(
            model=todo_list, display_selection='remaining')

        with self.assertTraitChanges(model_view, 'displayed_items', count=1):
            model_view.model = ToDoList(items=[item_1])

        self.assertEqual(len(model_view.displayed_items), 1)
        self.assertEqual(
            [controller.model for controller in model_view.displayed_items],
            [item_1])
        self.assertEqual(model_view.remaining, '1 item remaining')

    def test_model_view_none_remaining(self):
        # test 'remaining' property handles zero case
        item_1 = ToDoItem(description='Something to do', completed=True)
        item_2 = ToDoItem(description='Something else to do', completed=True)
        todo_list = ToDoList(items=[item_1, item_2])

        model_view = ToDoListModelView(model=todo_list)

        self.assertEqual(model_view.remaining, 'No items remaining')

    def test_model_view_plural_remaining(self):
        # test 'remaining' property handles plural case
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do')
        todo_list = ToDoList(items=[item_1, item_2])

        model_view = ToDoListModelView(model=todo_list)

        self.assertEqual(model_view.remaining, '2 items remaining')

    def test_model_view_new_item(self):
        # test that new item action works
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do', completed=True)
        todo_list = ToDoList(items=[item_1, item_2])

        model_view = ToDoListModelView(
            model=todo_list, display_selection='remaining')

        with self.assertTraitChanges(model_view, 'displayed_items', count=1):
            model_view.new_item(None)

        self.assertEqual(len(model_view.displayed_items), 2)
        self.assertEqual(
            [controller.model for controller in model_view.displayed_items],
            todo_list.remaining_items)
        self.assertEqual(model_view.remaining, '2 items remaining')
