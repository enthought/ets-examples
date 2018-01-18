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
This module provides standard trait definitions for cellular automata classes.
"""

from traits.api import Range

#: A trait that holds a valid state value.
StateValue = Range(0, 255)

#: A trait that holds a valid probability.
Probability = Range(0.0, 1.0)
