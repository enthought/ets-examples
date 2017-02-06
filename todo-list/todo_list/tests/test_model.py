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
Tests for To-do List Model Code
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from unittest import TestCase

from traits.testing.unittest_tools import UnittestTools

from todo_list.model import ToDoItem, ToDoList


class TestToDoItem(TestCase, UnittestTools):

    def test_to_do_item(self):
        # simple smoke test, since we have basically no logic
        todo = ToDoItem(description='Something to do')

        with self.assertTraitChanges(todo, 'completed', count=1):
            todo.completed = True


class TestToDoList(TestCase, UnittestTools):

    def test_to_do_list(self):
        # test that handlers work statically
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do', completed=True)
        todo_list = ToDoList(items=[item_1, item_2])

        self.assertEqual(todo_list.remaining_items, [item_1])
        self.assertEqual(todo_list.remaining, 1)

    def test_to_do_list_completed_changed(self):
        # test that handlers work when an item's status changes
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do')
        todo_list = ToDoList(items=[item_1, item_2])

        with self.assertTraitChanges(todo_list, 'remaining_items', count=1):
            with self.assertTraitChanges(todo_list, 'remaining', count=1):
                item_2.completed = True

        self.assertEqual(todo_list.remaining_items, [item_1])
        self.assertEqual(todo_list.remaining, 1)

    def test_to_do_list_changed(self):
        # test that handlers work when the list of items changes totally
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do', completed=True)
        todo_list = ToDoList(items=[item_1, item_2])

        item_3 = ToDoItem(description='New thing to do')
        item_4 = ToDoItem(description='Another new thing to do')

        with self.assertTraitChanges(todo_list, 'remaining_items', count=1):
            with self.assertTraitChanges(todo_list, 'remaining', count=1):
                todo_list.items = [item_3, item_4]

        self.assertEqual(todo_list.remaining_items, [item_3, item_4])
        self.assertEqual(todo_list.remaining, 2)

    def test_to_do_list_items_changed(self):
        # test that handlers work when the list of items is modified in-place
        item_1 = ToDoItem(description='Something to do')
        item_2 = ToDoItem(description='Something else to do', completed=True)
        todo_list = ToDoList(items=[item_1, item_2])

        item_3 = ToDoItem(description='New thing to do')

        with self.assertTraitChanges(todo_list, 'remaining_items', count=1):
            with self.assertTraitChanges(todo_list, 'remaining', count=1):
                todo_list.items.append(item_3)

        self.assertEqual(todo_list.remaining_items, [item_1, item_3])
        self.assertEqual(todo_list.remaining, 2)
