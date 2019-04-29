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
Forest Fire Parameter Exploration
=================================

This example shows parallel execution of multiple forest fire
simulations with parameters swept over a range of values to
collect and display statistics about the model.

In this example, we use a modified version of a forest fire
simulation with the following states:

- Empty cell: 0
- Healthy tree: 1
- Burning tree: 2
- Moldy tree: 3

Every tick:

- an empty cell can grow a tree
- fires are randomly started and burn down all connected trees
- crowded trees have a chance of contracting and dying from mold
  infection

The script runs the simulation with different values for the
likelihood of mold infection.  As the probability grows, a qualitative
decrease can be seen in the size and effect of fires, as the deaths
due to mold have the effect of breaking up large groups of trees into
less-connected groves, making it harder for fire to spread.
"""

import numpy as np

from cellular_automata.automata_recorder import AutomataRecorder, count_states
from cellular_automata.cellular_automaton import CellularAutomaton
from cellular_automata.rules.change_state_rule import ChangeStateRule
from cellular_automata.rules.forest import BurnGrovesRule, MoldRule


# State values
EMPTY = 0
TREE = 1
FIRE = 2
MOLD = 3


def simulation(p_mold, size, steps):
    """ Perform a simulation of a moldy forest, returning statistics.

    Parameters
    ----------
    p_mold : probability
        The probability that a crowded tree dies of mold.
    size : size tuple
        The number of cells in each direction for the simulation.
    steps : int
        The number of ticks to run the simulation for.

    Returns
    -------
    counts : array
        Array with shape (4, steps) of counts of each state at
        each tick.
    """
    np.random.seed(None)

    # trees grow
    grow = ChangeStateRule(
        from_state=EMPTY,
        to_state=TREE,
        p_change=0.0025
    )

    # fires are started, and all connected trees burn
    burn_groves = BurnGrovesRule()

    # crowded trees have a chance to be infected with mold
    mold = MoldRule(dead_state=MOLD, p_mold=p_mold)

    # trees which are infected with mold die
    mold_die = ChangeStateRule(
        from_state=MOLD,
        to_state=EMPTY,
        p_change=1.0
    )

    # fires are extinguished
    fire_out = ChangeStateRule(
        from_state=FIRE,
        to_state=EMPTY,
        p_change=1.0
    )

    forest = CellularAutomaton(
        shape=size,
        rules=[mold_die, fire_out, grow, burn_groves, mold],
    )

    # record the number of each state
    recorder = AutomataRecorder(automaton=forest, transform=count_states)

    forest.start()
    for i in range(steps):
        forest.step()

    return recorder.as_array()


if __name__ == '__main__':
    from joblib import Parallel, delayed
    import matplotlib.pyplot as plt

    SHAPE = (256, 256)
    N_STEPS = 4096
    N_SIMULATIONS = 16

    results = Parallel(n_jobs=4)(
        delayed(simulation)(p_mold, SHAPE, N_STEPS, count_states)
        for p_mold in np.logspace(-4, -1, N_SIMULATIONS)
    )

    for i, result in enumerate(results):
        # plot count of each non-empty state over time
        plt.subplot(N_SIMULATIONS, 2, 2*i+1)
        for state, color in [(TREE, 'g'), (FIRE, 'r'), (MOLD, 'c')]:
            plt.plot(result[state, :], c=color)

        # plot histogram
        plt.subplot(N_SIMULATIONS, 2, 2*i+2)
        plt.hist(
            np.log(result[result[1] != 0, 1]),
            bins=np.linspace(0, 10, 21)
        )
    plt.show()
