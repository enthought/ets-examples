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
This module provides tools for recording information about a cellular automata
over time as it evolves.  This includes the :py:class:`AutomataReader` class
which performs the actual recording of values, and a collection of callables
that transform states in useful ways.
"""
from functools import wraps

import numpy as np
from traits.api import Callable, HasStrictTraits, Instance, List, on_trait_change

from .cellular_automaton import CellularAutomaton


class AutomataRecorder(HasStrictTraits):
    """ An object that records changes to the states of a cellular automata.

    An optional :py:attr:`transform` function can be provided that will be used
    to compute derived values from the states (such as counts of different
    states) or only recording on certain time ticks.

    Recording happens on changes to the the :py:attr:`automaton.ticks` value.
    If the :py:attr:`transform` trait is :py:obj:`None`, then the current
    value of the automaton's states will be added to the record.
    If the :py:attr:`transform` trait is not :py:obj:`None` then that will
    be called with the automaton passed to it as the only argument, and any
    non-:py:obj:`None` value that is returned will be added to the
    :py:attr:`record` list.
    """

    #: The CellularAutomaton to record.
    automaton = Instance(CellularAutomaton)

    #: The record of states.
    record = List

    #: A function to call to compute the value to record.  This should accept
    #: a single CellularAutomaton as an argument and return an arbitrary value.
    transform = Callable

    # ------------------------------------------------------------------------
    # AutomataRecorder interface
    # ------------------------------------------------------------------------

    def as_array(self):
        """ Return the record as a single stacked array.

        This presumes that the recorded values are all arrays with compatible
        shapes to be stacked.
        """
        return np.stack(self.record)

    # ------------------------------------------------------------------------
    # object interface
    # ------------------------------------------------------------------------

    def __init__(self, automaton=None, **traits):
        super(AutomataRecorder, self).__init__(**traits)
        # ensure that the automaton is set _after_ everything is set up
        # this means in particular that we get first state if it is not None.
        if automaton is not None:
            self.automaton = automaton

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _record(self):
        """ Record the (possibly transformed) states.

        If the :py:attr:`transform` trait is not :py:obj:`None` then that will
        be called with the automaton passed to it as the only argument, and any
        non-:py:obj:`None` value that is returned will be added to the
        :py:attr:`record` list.

        Subclasses that want to do something more sophisticated can override
        this method.

        Parameters
        ----------
        states : array
            The states that will be recorded.
        """
        if self.automaton is None or self.automaton.states is None:
            return
        if self.transform is not None:
            value = self.transform(self.automaton)
        else:
            value = self.automaton.states

        if value is not None:
            self.record.append(value)

    # Trait change handlers --------------------------------------------------

    @on_trait_change('automaton:tick')
    def _time_updated(self):
        if self.automaton.tick == -1:
            # automaton was reset, dump
            self.record = []
        else:
            self._record()

    @on_trait_change('automaton')
    def _automaton_updated(self, automaton):
        # reset the record for the new automaton
        self.record = []
        self._record()


def count_states(automaton):
    """ A function that counts the unique states of the automata.

    This is suitable for use as the :py:attr:`transform` of an
    :py:class:`AutomataRecorder`.

    Parameters
    ----------
    automaton : CellularAutomaton
        The cellular automaton being analyzed.

    Returns
    -------
    counts : array
        A 1D array of size 256 containing the counts of each value.
    """
    states = automaton.states
    uniques, counts = np.unique(states, return_counts=True)
    full_counts = np.zeros(256, dtype=int)
    full_counts[uniques] = counts
    return full_counts


def call_if(test):
    """ Decorator factory that records automaton state only if test is True.

    Parameters
    ----------
    test : callable
        A callable that takes an automaton as input and returns a bool.

    Returns
    -------
    decorator : function
        The decorator that wraps the function with the test.
    """

    def decorator(fn):
        """ Decorator that records automaton state every only if test is True. """

        @wraps(fn)
        def f(automaton):
            if test(automaton):
                return fn(automaton)
            return None

        return f

    return decorator


def every_nth(n):
    """ Decorator factory that records automaton state every nth tick. """

    def is_nth(automaton):
        return automaton.tick % n == 0

    return call_if(is_nth)
