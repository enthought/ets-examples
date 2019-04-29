import numpy as np

from cellular_automata.automata_recorder import AutomataRecorder, count_states
from cellular_automata.cellular_automaton import CellularAutomaton
from cellular_automata.rules.change_state_rule import ChangeStateRule
from cellular_automata.rules.forest import BurnGrovesRule, MoldRule


def simulation(p_mold, size, steps, transform=None):
    np.random.seed(None)

    grow = ChangeStateRule(
        from_state=0,
        to_state=1,
        p_change=0.0025
    )
    burn_groves = BurnGrovesRule()
    mold = MoldRule(dead_state=3, p_mold=p_mold)
    mold_die = ChangeStateRule(
        from_state=3,
        to_state=0,
        p_change=1.0
    )
    fire_out = ChangeStateRule(
        from_state=2,
        to_state=0,
        p_change=1.0
    )

    forest = CellularAutomaton(
        shape=size,
        rules=[mold_die, fire_out, grow, burn_groves, mold],
    )
    recorder = AutomataRecorder(automaton=forest, transform=transform)

    forest.start()
    for i in range(steps):
        forest.step()

    return recorder.as_array()[:, 1:4].T


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
        plt.subplot(N_SIMULATIONS, 2, 2*i+1)
        for j, color in enumerate('grc'):
            plt.plot(result[j], c=color)
        plt.subplot(N_SIMULATIONS, 2, 2*i+2)
        plt.hist(np.log(result[1, result[1] != 0]), bins=np.linspace(0, 10, 21))
    plt.show()
