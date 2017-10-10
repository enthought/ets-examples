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
This script demonstrates the basic use of the cellular_automata library to
display `Elementary 1D Cellular Automata
<https://https://en.wikipedia.org/wiki/Elementary_cellular_automaton>`_ at the
command prompt.
"""

import click

from cellular_automata.cellular_automaton import CellularAutomaton
from cellular_automata.rules.elementary_1d_rule import Elementary1DRule
from cellular_automata.io.text import automaton_to_text
from cellular_automata.initializers.pattern_overlay import PatternOverlay


@click.command()
@click.option('--rule', default=30, help='rule number to use')
@click.option('--size', default=79, help='the number of cells')
@click.option('--pattern', default=u'●', help='the number of cells')
@click.option('--boundary', default='wrap',
              type=click.Choice(['wrap', 'empty', 'nearest']),
              help='how to treat the boundary')
@click.option('--ticks', default=40, help='number of simulation steps')
def main(rule, size, pattern, boundary, ticks):
    """ Run an elementary 1D cellular automaton. """
    pattern = [(0 if char == ' ' else 1) for char in pattern]

    # setup simulation
    rule = Elementary1DRule(rule_number=rule, boundary=boundary)
    pattern_overlay = PatternOverlay(pattern=pattern)
    world = CellularAutomaton(
        shape=(size,),
        initializers=[pattern_overlay],
        rules=[rule]
    )

    # initialize and display initial state
    world.start()
    print(automaton_to_text(world))

    # run
    for i in range(ticks):
        world.step()
        print(automaton_to_text(world))

if __name__ == '__main__':
    main()
