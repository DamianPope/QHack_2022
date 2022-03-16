#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np
from pennylane.templates import QuantumPhaseEstimation
#import specialized math functions
import math


dev = qml.device("default.qubit", wires=8)

def oracle_matrix(indices):
    """Return the oracle matrix for a secret combination.

    Args:
        - indices (list(int)): A list of bit indices (e.g. [0,3]) representing the elements that are map to 1.

    Returns:
        - (np.ndarray): The matrix representation of the oracle
    """

    # QHACK #

    #initialize array that stores unitary operator for Grover's oracle.    
    my_array=np.identity(16,dtype=int)

    #tag all "winner" elements with a minus sign
    for i in range(len(indices)):
        my_array[indices[i],indices[i]]=-1

    # QHACK #

    return my_array


def diffusion_matrix():

    # DO NOT MODIFY anything in this code block

    psi_piece = (1 / 2 ** 4) * np.ones(2 ** 4)
    ident_piece = np.eye(2 ** 4)
    return 2 * psi_piece - ident_piece


def grover_operator(indices):

    # DO NOT MODIFY anything in this code block

    return np.dot(diffusion_matrix(), oracle_matrix(indices))


dev = qml.device("default.qubit", wires=8)

@qml.qnode(dev)
def circuit(indices):
    """Return the probabilities of each basis state after applying QPE to the Grover operator

    Args:
        - indices (list(int)): A list of bits representing the elements that map to 1.

    Returns:
        - (np.tensor): Probabilities of measuring each computational basis state
    """

    # QHACK #

    target_wires = [0,1,2,3]
    estimation_wires = [4,5,6,7]

    # Build your circuit here

    #Only apply Hadamards to target qubits as quantum phase estimation algorithm automatically applies them to estimation qubits
    for i in range(4):
        qml.Hadamard(wires=i)
    
    QuantumPhaseEstimation(grover_operator(indices),target_wires=target_wires,estimation_wires=estimation_wires)
     
    # QHACK #

    return qml.probs(estimation_wires)

def number_of_solutions(indices):
    """Implement the formula given in the problem statement to find the number of solutions from the output of your circuit

    Args:
        - indices (list(int)): A list of bits representing the elements that map to 1.

    Returns:
        - (float): number of elements as estimated by the quantum counting algorithm
    """

    # QHACK #
    
    #store list of probabilities of measuring estimation qubits to be in each of the 16 computational basis states in circuitProbs
    circuitProbs=circuit(indices)
     
    #find the computational basis state with the highest probability
    maxProb = circuitProbs[0]
    maxIndex = 0

    for i in range(1,len(circuitProbs)):
        if circuitProbs[i] > maxProb:
            maxProb = circuitProbs[i]
            maxIndex = i

    theta = maxIndex*3.14159/8
    M = 16*(math.sin(theta/2))**2

    return M
    # QHACK #

def relative_error(indices):
    """Calculate the relative error of the quantum counting estimation

    Args:
        - indices (list(int)): A list of bits representing the elements that map to 1.

    Returns: 
        - (float): relative error
    """

    # QHACK #

    rel_err = ((number_of_solutions(indices)-len(indices))/len(indices))*100

    # QHACK #

    return rel_err

if __name__ == '__main__':
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    lst=[int(i) for i in inputs]
    output = relative_error(lst)
    print(f"{output}")