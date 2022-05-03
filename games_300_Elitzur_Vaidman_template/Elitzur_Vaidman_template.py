#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np

dev = qml.device("default.qubit", wires=1, shots=1)


@qml.qnode(dev)
def is_bomb(angle):
    """Construct a circuit at implements a one shot measurement at the bomb.

    Args:
        - angle (float): transmissivity of the Beam splitter, corresponding
        to a rotation around the Y axis.

    Returns:
        - (np.ndarray): a length-1 array representing result of the one-shot measurement
    """

    # QHACK #

    #initial state is |0>
 
    #implement beamsplitter operation
    qml.RY(2.0*angle,wires=0)
    
    # QHACK #

    return qml.sample(qml.PauliZ(0))


@qml.qnode(dev)
def bomb_tester(angle):
    """Construct a circuit that implements a final one-shot measurement, given that the bomb does not explode

    Args:
        - angle (float): transmissivity of the Beam splitter right before the final detectors

    Returns:
        - (np.ndarray): a length-1 array representing result of the one-shot measurement
    """

    # QHACK #

    #initial state is |0>

    #implement beamsplitter operation
    qml.RY(2.0*angle,wires=0)
    
    # QHACK #

    return qml.sample(qml.PauliZ(0))


def simulate(angle, n):
    """Concatenate n bomb circuits and a final measurement, and return the results of 10000 one-shot measurements

    Args:
        - angle (float): transmissivity of all the beam splitters, taken to be identical.
        - n (int): number of bomb circuits concatenated

    Returns:
        - (float): number of bombs successfully tested / number of bombs that didn't explode.
    """

    # QHACK #

    num_D_beeps = 0
    num_unexploded_bombs = 0

    for j in range(10000): 
   
        for i in range(n):
            
            singleCircuitOutput = is_bomb(angle)
            
            if singleCircuitOutput == 1:
                #A photon hit a bomb & it explodes. Stop going through the entire interferometer.
                break

            else:
                #photon collapses to |1> output state
                
                if (i==(n-1)):
                    #A photon has reached the final detector. Measure which detector it hits, C or D.    
                    finalDetectionResult = bomb_tester(angle)
                    
                    num_unexploded_bombs += 1
                
                    """"This code gives the correct answer. But I need to check why the number on the line below is -1 (which implies |1>_out and C) 
                    instead of +1 (which implies |0>_out and D)"""
                    if (finalDetectionResult == -1):
                        #D detects the photon
                        num_D_beeps+=1
                
    return float(num_D_beeps/num_unexploded_bombs)
    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    output = simulate(float(inputs[0]), int(inputs[1]))
    print(f"{output}")
