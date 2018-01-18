# Copyright (c) 2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Instance, List

from cellular_automata.automata_traits import StateValue
from .abstract_rule import AbstractRule


class MultiRule(AbstractRule):

    #: The rules to use to compute the changes within the mask.
    rules = List(Instance(AbstractRule))

    def step(self, states):
        """ Run a step of each rule from the rules list in order.

        Parameters
        ----------
        states : array
            An array holding the current states of the automata.

        Returns
        -------
        states : array
            The new states of the automata after the rule has been applied.
        """
        states = super(MaskStateMultiRule, self).step(states)

        for rule in self.rules:
            states = rule.step(states)

        return states

    def check_states(self, states):
        """ Check that the states match what each rule expects as input.

        Parameters
        ----------
        states : array
            An array holding the current states of the automata.

        Raises
        ------
        ValueError
            If the states are not compatible with the rule.
        """
        super(MultiRule, self).check_states(states)

        for rule in self.rules:
            rule.check_states(states)



class MaskStateMultiRule(MultiRule):

    #: The state that the changes should be applied to.
    mask_state = StateValue(0)

    def step(self, states):
        states = super(MaskStateMultiRule, self).step(states)

        changed_states = states.copy()
        for rule in self.rules:
            changed_states = rule.step(changed_states)

        mask = (states == self.mask_state)
        states[mask] = changed_states[mask]

        return states
