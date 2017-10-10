import numpy as np

from cellular_automata.automata_recorder import AutomataRecorder
from cellular_automata.cellular_automaton import CellularAutomaton
from cellular_automata.rules.change_state_rule import ChangeStateRule
from cellular_automata.rules.forest import SlowBurnRule
from cellular_automata.io.image import save_image_sequence


def simulation(size, steps):
    np.random.seed(None)

    grow = ChangeStateRule(
        from_state=0,
        to_state=1,
        p_change=0.0025
    )
    lightning = ChangeStateRule(
        from_state=1,
        to_state=2,
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
    palette[1] = [0, 255, 0]
    palette[2] = [255, 0, 0]
    palette[3] = [255, 255, 255]

    save_image_sequence(recorder, 'test.gif', palette, 100)

if __name__ == '__main__':
    SHAPE = (256, 256)
    N_STEPS = 4096
    N_SIMULATIONS = 16

    simulation(SHAPE, N_STEPS)
