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
from scipy import ndimage

from traits.api import Array, Constant, Enum, Property, Range, cached_property

from cellular_automata.automata_traits import StateValue
from .base_rules import NDimRule

REVERSE_PERMUTATION = [0, 4, 2, 6, 1, 5, 3, 7]


class Elementary1DRule(NDimRule):
    """ Rule implementing an elementary 1D cellular automata.

    This uses Wolfram's rule numbering scheme to identify the rules and
    scipy.ndimage to handle the boundary conditions.

    Notes
    -----

    See `Wikipedia
    <https://en.wikipedia.org/wiki/Elementary_cellular_automaton>`_ for further
    information on how these automata work.
    """

    # Elementary1DRule Traits ------------------------------------------------

    #: The number of the rule.
    rule_number = Range(0, 255)

    #: The state value for "empty" cells.
    empty_state = StateValue(0)

    #: The state value for "filled" cells.
    filled_state = StateValue(1)

    #: The bit-mask corresponding to the rule.
    bit_mask = Property(Array(shape=(8,), dtype=bool),
                        depends_on='rule_number')

    #: The boundary mode to use.
    boundary = Enum('empty', 'filled', 'nearest', 'wrap', 'reflect')

    # NDimRule Traits --------------------------------------------------------

    #: These are 1-dimensional only rules.
    ndim = Constant(1)

    # ------------------------------------------------------------------------
    # Elementary1DRule interface
    # ------------------------------------------------------------------------

    def reflect(self):
        """ Reflect the cellular automata left-to-right. """
        self.bit_mask = self.bit_mask[REVERSE_PERMUTATION]

    def complement(self):
        """ Complement the cellular automata replacing 1's with 0's throughout. """
        self.bit_mask = ~self.bit_mask[::-1]

    # ------------------------------------------------------------------------
    # AbstractRule interface
    # ------------------------------------------------------------------------

    def step(self, states):
        """ Apply the specified rule to the states.

        Parameters
        ----------
        states : array
            An array holding the current states of the automata.

        Returns
        -------
        states : array
            The new states of the automata after the rule has been applied.
        """
        states = super(NDimRule, self).step(states)

        wrap_args = {'mode': self.boundary}
        if self.boundary == 'empty':
            wrap_args['mode'] = 'constant'
            wrap_args['cval'] = 0
        elif self.boundary == 'filled':
            wrap_args['mode'] = 'constant'
            wrap_args['cval'] = 1

        filled = (states == self.filled_state)
        filled = ndimage.generic_filter1d(
            filled, self._rule_filter, filter_size=3, **wrap_args)

        states = np.full(filled.shape, self.empty_state, dtype='uint8')
        states[filled] = self.filled_state
        return states

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _rule_filter(self, iline, oline):
        """ Kernel to compute values in generic filter """
        index = (iline[:-2] * 4 + iline[1:-1] * 2 + iline[2:]).astype('uint8')
        oline[...] = self.bit_mask[index]

    # Trait properties -------------------------------------------------------

    @cached_property
    def _get_bit_mask(self):
        bits = np.unpackbits(np.array([self.rule_number], dtype='uint8'))[::-1]
        return bits.astype(bool)

    def _set_bit_mask(self, bits):
        bits = np.asarray(bits, dtype=bool)
        self.rule_number = int(np.packbits(bits[::-1])[0])
