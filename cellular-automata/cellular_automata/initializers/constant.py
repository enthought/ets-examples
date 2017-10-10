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

from cellular_automata.abstract_initializer import AbstractInitializer
from cellular_automata.automata_traits import StateValue

class Constant(AbstractInitializer):
    """ Initialize the states to the constant initial value. """

    #: Initial state value.
    initial_value = StateValue(0)

    def initialize_states(self, states):
        """ Initialize the states to the constant initial value.

        Parameters
        ----------
        states : array
            The initial array of states to be modified.

        Returns
        -------
        states : array
            The states after having been modified by the initializer.
        """
        states.fill(self.initial_value)
        return states
