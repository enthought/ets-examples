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
