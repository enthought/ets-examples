# -*- coding: utf-8 -*-
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
This module provides routines to assist display of cellular automata in
textual form.
"""

from collections import defaultdict


DEFAULT_PALETTE = defaultdict(lambda: u'●', {0: u' '})

FOREST_PALETTE = defaultdict(
    lambda: u'●',  # default
    {
        0: u' ',
        1: u'\U0001F332',  # evergreen tree
        2: u'\U0001f525',  # fire
        3: u'\U0001F342',  # falling leaves
    }
)


def automaton_to_text(automaton, palette=DEFAULT_PALETTE):
    """ Generate a text representation of the automaton states.

    Parameters
    ----------
    automaton : CellularAutomaton instance
        The automaton to render.
    palette : str
        A string in which the symbol of the nth character will be used to
        represent the nth state.

    Returns
    -------
    text : str
        The textual representation of the state of the automaton.
    """
    states = automaton.states

    joiners = [u'']
    if states.ndim >= 2:
        joiners = [u'\n'] + joiners
        if states.ndim >= 3:
            joiners = [u'\n\n\n'] * (states.ndim - 2) + joiners

    return _render_states(states, palette, joiners)


def _render_states(states, palette, joiners):
    """ Recursively render dimensions of the states, joining with next joiner. """
    joiner = joiners[0]
    if len(joiners) == 1:
        parts = (palette[state] for state in states)
    else:
        parts = (_render_states(sheet, joiners[1:]) for sheet in states)
    return joiner.join(parts)
