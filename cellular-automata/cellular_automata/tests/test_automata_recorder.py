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

from ..automata_recorder import AutomataRecorder, count_states
from ..cellular_automaton import CellularAutomaton


class TestCountNeighboursRule(TestCase, UnittestTools):

    def test_simple_recording(self):
        # a do-nothing automaton
        states = np.zeros(shape=(10, 10), dtype='uint8')
        automaton = CellularAutomaton(states=states)

        recorder = AutomataRecorder(automaton)

        self.assertEqual(len(recorder.record), 1)
        self.assertIs(recorder.record[0], states)

        with self.assertTraitChanges(recorder, 'record_items', 1):
            automaton.step()

        self.assertEqual(len(recorder.record), 2)
        assert_array_equal(recorder.record[1], states)

    def test_transform_recording(self):
        # a do-nothing automaton
        states = np.zeros(shape=(10, 10), dtype='uint8')
        automaton = CellularAutomaton(states=states)

        recorder = AutomataRecorder(automaton, transform=count_states)
        expected_counts = np.zeros(256, dtype=int)
        expected_counts[0] = 100

        self.assertEqual(len(recorder.record), 1)
        assert_array_equal(recorder.record[0], expected_counts)

        with self.assertTraitChanges(recorder, 'record_items', 1):
            automaton.step()

        self.assertEqual(len(recorder.record), 2)
        assert_array_equal(recorder.record[1], expected_counts)
