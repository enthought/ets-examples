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
Forest Fire Simulation
======================

This example runs cellular automata simulation and saves the results as a
GIF image.

In this example, we use a modified version of a forest fire
simulation with the following states:

- Empty cell: 0
- Healthy tree: 1
- Burning tree: 2

Every tick:

- an empty cell can grow a tree
- lightning randomly starts fires in trees
- fire spreads to neighbouring trees and trees which were previously
  on fire die

See also
--------

This model was originally introduced in:

    Drossel, B. and Schwabl, F. (1992),
    "Self-organized critical forest-fire model."
    Phys. Rev. Lett. 69, 1629–1632.

"""

import numpy as np

from cellular_automata.automata_recorder import AutomataRecorder
from cellular_automata.cellular_automaton import CellularAutomaton
from cellular_automata.rules.change_state_rule import ChangeStateRule
from cellular_automata.rules.forest import SlowBurnRule
from cellular_automata.io.image import save_image_sequence


# State values
EMPTY = 0
TREE = 1
FIRE = 2

# State colors
GREEN = [0, 255, 0]
RED = [255, 0, 0]
WHITE = [255, 255, 255]


def simulation(size, steps):
    """ Perform a simulation of a forest fire, outputting a GIF.

    Parameters
    ----------
    size : size tuple
        The number of cells in each direction for the simulation.
    steps : int
        The number of ticks to run the simulation for.
    """
    np.random.seed(None)

    grow = ChangeStateRule(
        from_state=EMPTY,
        to_state=TREE,
        p_change=0.0025
    )
    lightning = ChangeStateRule(
        from_state=TREE,
        to_state=FIRE,
        p_change=1e-5,
    )
    burn = SlowBurnRule()

    forest = CellularAutomaton(
        shape=size,
        rules=[grow, lightning, burn],
    )
    recorder = AutomataRecorder(automaton=forest)

    forest.start()
    for i in range(steps):
        forest.step()

    palette = np.zeros((256, 3), dtype='uint8')
    palette[1] = GREEN
    palette[2] = RED

    save_image_sequence(recorder, 'test.gif', palette, 100)


if __name__ == '__main__':
    SHAPE = (256, 256)
    N_STEPS = 4096

    simulation(SHAPE, N_STEPS)
