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
A collection of base classes for common behaviour of certain rule types.
"""

from traits.api import Array, Enum, Int, Property

from cellular_automata.abstract_rule import AbstractRule


class NDimRule(AbstractRule):
    """ A rule which expects the state to be N-dimensional. """

    # NDimRule Traits --------------------------------------------------------

    #: The expected dimensionality of the state.
    ndim = Int(2)

    # ------------------------------------------------------------------------
    # AbstractRule interface
    # ------------------------------------------------------------------------

    def check_states(self, states):
        """ Check that the state has the expected dimensionality.

        This raises a value error if the states array's dimension is not equal
        to the value of the :py:attr:`ndim` trait.

        Parameters
        ----------
        states : array
            An array holding the current states of the automata.

        Raises
        ------
        ValueError
            If the states has incompatible dimension.
        """
        if states.ndim != self.ndim:
            msg = "States are expected to be {}-dimensional, but have {} dimensions."  # noqa: E501
            raise ValueError(msg.format(self.ndim, states.ndim))


class StructureRule(NDimRule):
    """ A rule which uses an n-dimensional structuring array.

    The dimensionality of the cellular automaton must match that of the
    :py:attr:`structure` array.
    """

    # StructureRule Traits ---------------------------------------------------

    #: The structure to use for determining neighbours.
    structure = Array(dtype=bool)

    # NDimRule Traits --------------------------------------------------------

    #: The dimension should match the dimension of the structure.
    ndim = Property(Int, depends_on='structure')

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    # Trait defaults ---------------------------------------------------------

    def _get_ndim(self):
        return self.structure.ndim

    def _structure_default(self):
        import numpy as np
        return np.ones(shape=(3, 3), dtype=bool)


class CountNeighboursRule(StructureRule):
    """ A rule which needs the count of neighbours.

    The :py:attr:`structure` array is used to determine which cells are
    counted as neighbours.
    """

    # CountNeighboursRule Traits ---------------------------------------------

    #: The boundary mode to use.
    boundary = Enum('empty', 'filled', 'nearest', 'wrap', 'reflect')

    # ------------------------------------------------------------------------
    # CountNeighboursRule interface
    # ------------------------------------------------------------------------

    def count_neighbours(self, mask):
        """ Return the count of the neighbours according to the mask. """
        from scipy.ndimage.filters import convolve

        mask = mask.astype('uint8')
        filter_args = {'mode': self.boundary}
        if self.boundary == 'empty':
            filter_args['mode'] = 'constant'
            filter_args['cval'] = 0
        elif self.boundary == 'filled':
            filter_args['mode'] = 'constant'
            filter_args['cval'] = 1

        counts = convolve(mask, self.structure, **filter_args)

        return counts

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    # Trait defaults ---------------------------------------------------------

    def _structure_default(self):
        import numpy as np
        return np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1],
        ], dtype=bool)
