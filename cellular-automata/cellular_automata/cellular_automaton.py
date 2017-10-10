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
This module contains the main class for a cellular automata simulation.
"""
import numpy as np
from traits.api import Array, HasStrictTraits, Int, Instance, List, Property

from .abstract_initializer import AbstractInitializer
from .abstract_rule import AbstractRule


class CellularAutomaton(HasStrictTraits):
    """ Class for general cellular automata.

    The class holds array of unsigned bytes where the labels are intended to be
    different states that the cell can take.  States have human readable
    names associated with them.  The states evolve via a list of rules, applied
    in order, which manipulate the state array.
    """

    #: The current time tick.  Listen to this for updates to the automaton.
    tick = Int(-1)

    #: An array holding the states of the cellular automata.
    states = Array(dtype='uint8')

    #: The shape of the array
    shape = Property(depends_on='states')

    #: The list of initializers to apply, in order.
    initializers = List(Instance(AbstractInitializer))

    #: The list of rules to apply, in order.
    rules = List(Instance(AbstractRule))

    # ------------------------------------------------------------------------
    # CellularAutomata interface
    # ------------------------------------------------------------------------

    def start(self):
        """ Create the initial states of the automaton. """
        if self.tick != -1:
            raise ValueError("Automaton has already started")

        states = self.states
        for initializer in self.initializers:
            states = initializer.initialize_states(states)

        self.states = states
        self.tick = 0

    def step(self):
        """ Advance the cellular automaton one step through time.

        This will change the states array after all rules have had a chance to
        apply their changes.
        """
        states = self.states.copy()
        for rule in self.rules:
            states = rule.step(states)
        self.states = states
        self.tick += 1

    def reset(self):
        """ Reset the simulation to a pre-start state. """
        self.states = np.zeros(self.shape, dtype='uint8')
        self.tick = -1

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def __init__(self, **traits):
        shape = traits.pop('shape', None)
        if shape is not None:
            states = np.zeros(shape, dtype='uint8')
            traits.setdefault('states', states)
        elif 'states' not in traits:
            raise ValueError("Must specify either shape or initial states")
        super(CellularAutomaton, self).__init__(**traits)

    # Trait properties -------------------------------------------------------

    def _get_shape(self):
        return self.states.shape

    def _set_shape(self, value):
        self.states.shape = value
