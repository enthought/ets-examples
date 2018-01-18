# Copyright (c) 2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from scipy import ndimage

from traits.api import Trait

from cellular_automata.automata_traits import StateValue
from .base_rules import StructureRule


class BinaryMorphologyRule(StructureRule):
    """ A rule that applies a morphology operation to a foreground state.

    Cells which were part of the foreground but are not after the operation
    are set to the specified background state value.
    """

    #: The state representing new background values.
    background_state = StateValue(0)

    #: The state representing foreground values.
    foreground_state = StateValue(1)

    operation = Trait('dilation', {
        'dilation': ndimage.binary_dilation,
        'erosion': ndimage.binary_erosion,
        'opening': ndimage.binary_opening,
        'closing': ndimage.binary_closing,
        'propagation': ndimage.binary_propagation,
        'fill_holes': ndimage.binary_fill_holes,
    })

    def step(self, states):
        """ Apply a binary morphology operation to "foreground" state cells.

        Cells which were part of the foreground but are not after the operation
        are set to the specified background state value.

        Parameters
        ----------
        states : array
            An array holding the current states of the automaton.

        Returns
        -------
        states : array
            The new states of the automaton after the rule has been applied.
        """
        states = super(BinaryMorphologyRule, self).step(states)

        foreground = (states == self.foreground_state)
        binary_mask = self.operation_(
            input=foreground,
            structure=self.structure,
        )

        states[binary_mask] = self.foreground_state
        states[foreground & ~binary_mask] = self.background_state

        return states
