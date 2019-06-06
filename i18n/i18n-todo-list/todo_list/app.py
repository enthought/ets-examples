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
This module provides the application infrastructure to run the to-do list
application.  It parses command-line arguments into to do items and starts
the TraitsUI application.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import argparse
from gettext import bindtextdomain, gettext as _, textdomain
import pkg_resources


TRANSLATIONS_DIR = pkg_resources.resource_filename(__name__, 'translations')


def handle_arguments():
    """ Parse commandline arguments and return list of items

    Allowed arguments are as many ``--todo`` optional arguments followed
    by the text of an item.
    """
    parser = argparse.ArgumentParser(
        description=_('To-do list TraitsUI application.')
    )
    parser.add_argument(
        '--todo',
        action='append',
        help=_('to-do list item'),
        metavar=_('ITEM'),
        default=[],
    )
    args = parser.parse_args()
    return args.todo


def main():
    """ The application entry-point """
    # set up the gettext translation infrastructure
    bindtextdomain('todo-list', TRANSLATIONS_DIR)
    textdomain('todo-list')

    # parse the arguments
    items = handle_arguments()

    # defer TraitsUI dependent imports until _ is installed in builtins
    from todo_list.model import ToDoList, ToDoItem
    from todo_list.view import ToDoListModelView

    # set up the model
    todo_list = ToDoList(
        items=[ToDoItem(description=item) for item in items]
    )

    # run the application
    model_view = ToDoListModelView(model=todo_list)
    model_view.configure_traits()


if __name__ == '__main__':
    main()
