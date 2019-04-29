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

from ..elementary_1d_rule import Elementary1DRule

class TestElementary1DRule(TestCase, UnittestTools):

    def test_check_states(self):
        rule = Elementary1DRule()

        state = np.zeros(shape=(100, 100), dtype='uint8')

        with self.assertRaises(ValueError):
            rule.check_states(state)

        with self.assertRaises(ValueError):
            rule.step(state)

    def test_bit_mask(self):
        rule = Elementary1DRule()

        assert_array_equal(rule.bit_mask, [0, 0, 0, 0, 0, 0, 0, 0])

        with self.assertTraitChanges(rule, 'bit_mask', 1):
            rule.rule_number = 30

        assert_array_equal(rule.bit_mask, [0, 1, 1, 1, 1, 0, 0, 0])

        with self.assertTraitChanges(rule, 'rule_number', 1):
            rule.bit_mask = [0, 1, 1, 1, 1, 1, 0, 0]

        rule.rule_number = 62

    def test_rule_30(self):
        rule = Elementary1DRule(rule_number=30)
        state = np.zeros(shape=8, dtype='uint8')
        state[4] = 1

        state = rule.step(state)
        assert_array_equal(state, [0, 0, 0, 1, 1, 1, 0, 0])

        state = rule.step(state)
        assert_array_equal(state, [0, 0, 1, 1, 0, 0, 1, 0])

        state = rule.step(state)
        assert_array_equal(state, [0, 1, 1, 0, 1, 1, 1, 1])

        state = rule.step(state)
        assert_array_equal(state, [1, 1, 0, 0, 1, 0, 0, 0])

    def test_reflection(self):
        rule = Elementary1DRule(rule_number=30)
        with self.assertTraitChanges(rule, 'rule_number', 1):
            rule.reflect()
        self.assertEqual(rule.rule_number, 86)

    def test_complement(self):
        rule = Elementary1DRule(rule_number=30)
        with self.assertTraitChanges(rule, 'rule_number', 1):
            rule.complement()
        self.assertEqual(rule.rule_number, 135)
