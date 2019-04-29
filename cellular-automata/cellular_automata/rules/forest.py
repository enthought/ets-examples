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
Rules that allow simple simulations of forest fire behaviour.
"""

import numpy as np
from scipy import ndimage

from traits.api import Int

from cellular_automata.automata_traits import Probability, StateValue
from .base_rules import CountNeighboursRule, StructureRule


#: The default structure to use for fires.  The central cell is blank to model
#: the fire burning out after one tick.
FIRE_STRUCTURE = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0],
], dtype=bool)


class BurnRule(StructureRule):
    """ A rule that sets on fire burnable cells that neighbour a burning cell.

    Neighbouring cells are determined by a connectivity structure.
    """
    # BurnRule Traits --------------------------------------------------------

    #: The state value for burnt cells.
    burnt_state = StateValue(0)

    #: The state value for burnable cells.
    burnable_state = StateValue(1)

    #: The state value for burning cells.
    burning_state = StateValue(2)

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _structure_default(self):
        return FIRE_STRUCTURE


class SlowBurnRule(BurnRule):
    """ A rule that sets on fire burnable cells that neighbour a burning cell.

    Neighbouring cells are determined by a connectivity structure.  Cells which
    were burning but are no longer after a step is performed are replaced by
    cells with the burnt state value.

    This rule models the evolution of a fire, where a particular fire may last
    many ticks.
    """

    # ------------------------------------------------------------------------
    # AbstractRule interface
    # ------------------------------------------------------------------------

    def step(self, states):
        states = super(SlowBurnRule, self).step(states)

        burning = (states == self.burning_state)
        burnable_mask = (states == self.burnable_state)

        new_burning = ndimage.binary_dilation(
            burning, self.structure, mask=burnable_mask, border_value=0,
        )

        states[new_burning] = self.burning_state
        states[burning] = self.burnt_state

        return states


class BurnGrovesRule(BurnRule):
    """ A rule that burns down entire burnable connected components.

    For this rule, first all existing fires evolve to burn out, and are
    replaced with the burnt state value. Then random cells are selected for
    the start of a fire, and where those cells are burnable, the connected
    component of the cell is set on fire. Connected components are determined
    by the connectivity structure.

    This rule models the effects of a fire where a partiuclar fire lasts only
    one tick but potentially covers a large area.
    """

    # BurnGrovesRule Traits --------------------------------------------------

    #: The probability of a fire starting in a particular cell.
    p_fire = Probability(5e-6)

    # ------------------------------------------------------------------------
    # AbstractRule interface
    # ------------------------------------------------------------------------

    def step(self, states):
        states = super(BurnGrovesRule, self).step(states)

        burnable = (states == self.burnable_state)
        strikes = (np.random.uniform(size=states.shape) < self.p_fire)
        groves, num_groves = ndimage.label(burnable)

        burning_groves = np.unique(groves[strikes & burnable])
        for grove in burning_groves:
            states[groves == grove] = self.burning_state

        return states


class MoldRule(CountNeighboursRule):
    """ A rule that kills overcrowded cells with some probability. """

    # MoldRule Traits --------------------------------------------------------

    #: The state value for dead cells.
    dead_state = StateValue(0)

    #: The state value for live cells.
    live_state = StateValue(1)

    #: The number of neighbours required to make a tree susceptible to mold.
    critical_density = Int(3)

    #: The probability of death if susceptible to mold.
    p_mold = Probability(3e-3)

    # ------------------------------------------------------------------------
    # AbstractRule interface
    # ------------------------------------------------------------------------

    def step(self, states):
        states = super(MoldRule, self).step(states)

        live = (states == self.live_state)
        count = self.count_neighbours(live)

        mold = live & (count >= self.critical_density)
        if self.p_mold < 1.0:
            mold &= (np.random.uniform(size=states.shape) < self.p_mold)

        states[mold] = self.dead_state

        return states

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    # Trait defaults ---------------------------------------------------------

    def _structure_default(self):
        return FIRE_STRUCTURE
