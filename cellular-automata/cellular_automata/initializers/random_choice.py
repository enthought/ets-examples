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
from scipy import stats
from traits.api import Array, Property, cached_property

from cellular_automata.abstract_initializer import AbstractInitializer


class RandomChoice(AbstractInitializer):
    """ Create initial states using a discrete random variable. """

    #: Initial values to choose from.
    distributon = Array(shape=(256,), dtype=float)

    #: A scipy stats random variable matching the distribution.
    random_variable = Property(depends_on='distribution')

    def initialize(self, states):
        """ Initialize the states according to the rule.

        Parameters
        ----------
        states : array
            The array to initialize.

        Returns
        -------
        states : array
            The initialized array.
        """
        states[:] = self.random_variable.rvs(size=states.shape)
        return states

    @classmethod
    def from_states(self, states, probs=None):
        """ Create a RandomChoice instance from states and probabilities.

        Parameters
        ----------
        states : list of int
            The possible state values.

        """
        if probs is None:
            n = len(states)
            probs = [1.0/n] * n

        distribution = np.zeros(256, dtype=float)
        distribution[states] = probs
        return distribution

    @cached_property
    def _get_random_variable(self):
        if self.distributon is None:
            return None

        pk = self.distributon
        xk = np.arange(256)
        mask = (pk != 0)
        rv = stats.rv_discrete(values=(xk[mask], self.distribution[mask]))
        return rv
