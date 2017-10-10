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
The module provides a rule that changes all cells from one state to another
with some probability.
"""

import numpy as np

from cellular_automata.abstract_rule import AbstractRule
from cellular_automata.automata_traits import Probability, StateValue


class ChangeStateRule(AbstractRule):
    """ Change states with one value to another at some probability.

    This can be used to mimic random growth or death processes.  When the
    probability is one, then this can be used to
    """

    # ChangeStateRule Traits -------------------------------------------------

    #: The state value to change.
    from_state = StateValue(0)

    #: The state value to change to.
    to_state = StateValue(1)

    #: The probability of a cell changing value.
    p_change = Probability(1.0)

    # ------------------------------------------------------------------------
    # AbstractRule interface
    # ------------------------------------------------------------------------

    def step(self, states):
        states = super(ChangeStateRule, self).step(states)

        mask = (states == self.from_state)
        if self.p_change < 1.0:
            mask &= (np.random.uniform(size=states.shape) < self.p_change)

        states[mask] = self.to_state

        return states
