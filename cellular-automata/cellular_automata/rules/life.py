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
Rules for implementing Conway's Game of Life and related cellular automata.
"""

import numpy as np

from traits.api import Int, Set

from cellular_automata.automata_traits import StateValue
from .base_rules import CountNeighboursRule


class LifeRule(CountNeighboursRule):
    """ A rule that implements Conway's Game of Life.

    Cells are either alive or dead.  On any turn, alive cells with one of
    :py:attr:`survive_counts` neighbours remain alive, otherwise they die;
    while dead cells with one of :py:attr:`born_counts` neighbours become
    alive.
    """

    #: The state value for dead cells.
    dead_state = StateValue(0)

    #: The state value for live cells.
    live_state = StateValue(1)

    #: The neighbour counts for a cell to be born.
    born_counts = Set(Int, {3})

    #: The neighbour counts for a cell to survive.
    survive_counts = Set(Int, {2, 3})

    # ------------------------------------------------------------------------
    # AbstractRule interface
    # ------------------------------------------------------------------------

    def step(self, states):
        states = super(LifeRule, self).step(states.copy())

        live = (states == self.live_state)

        counts = self.count_neighbours(live)
        count_masks = {}

        born = np.zeros(states.shape, dtype=bool)
        for count in self.born_counts:
            if count not in count_masks:
                count_masks[count] = (counts == count)
            born |= count_masks[count]
        born &= ~live

        survived = np.zeros(states.shape, dtype=bool)
        for count in self.survive_counts:
            if count not in count_masks:
                count_masks[count] = (counts == count)
            survived |= count_masks[count]
        died = live & ~survived

        states[born] = self.live_state
        states[died] = self.dead_state

        return states
