# Copyright (c) 2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import numpy as np

from cellular_automata.abstract_initializer import AbstractInitializer
from cellular_automata.automata_traits import Probability, StateValue

class RandomOverlay(AbstractInitializer):
    """ Initialize the states to an initial value with some probability. """

    #: State value to overlay.
    overlay_value = StateValue(0)

    #: The probability that a cell gets that value.
    p_value = Probability(0.5)

    def initialize_states(self, states):
        """ Initialize a random set of states to the overlay value.

        Parameters
        ----------
        states : array
            The initial array of states to be modified.

        Returns
        -------
        states : array
            The states after having been modified by the initializer.
        """
        overlaid_mask = (np.random.uniform(states.shape) < self.p_value)
        states[overlaid_mask] = self.overlay_value
        return states
