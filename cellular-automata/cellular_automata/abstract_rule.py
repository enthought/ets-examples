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
This module provides the abstract base class to use for all cellular automata
rules.  Rules must have a step function that transforms the old states array
to a new states array.
"""

from traits.api import ABCHasStrictTraits


class AbstractRule(ABCHasStrictTraits):
    """ Abstract bace class for cellular automata rules. """

    # ------------------------------------------------------------------------
    # AbstractRule interface
    # ------------------------------------------------------------------------

    def step(self, states):
        """ Apply the rule for a single step.

        The default rule does nothing but validate inputs.

        Parameters
        ----------
        states : array
            An array holding the current states of the automaton.

        Returns
        -------
        states : array
            The new states of the automaton after the rule has been applied.
        """
        self.check_states(states)
        return states

    def check_states(self, states):
        """ Check that the state matches what the rule expects as input.

        This can be used to check that the dimensionality of the state is
        expected.

        Parameters
        ----------
        states : array
            An array holding the current state of the automaton.

        Raises
        ------
        ValueError
            If the states are not compatible with the rule.
        """
        pass
