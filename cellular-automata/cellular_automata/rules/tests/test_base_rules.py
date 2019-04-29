# Copyright (c) 2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal

from traits.testing.unittest_tools import UnittestTools

from ..base_rules import CountNeighboursRule


class TestCountNeighboursRule(TestCase, UnittestTools):

    def test_count_neighbours(self):
        rule = CountNeighboursRule()

        mask = np.ones(shape=(3, 3), dtype='uint8')

        counts = rule.count_neighbours(mask)

        assert_array_equal(counts, [[3, 5, 3], [5, 8, 5], [3, 5, 3]])
