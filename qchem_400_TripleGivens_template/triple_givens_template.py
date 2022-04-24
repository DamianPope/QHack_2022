import sys
import pennylane as qml
from pennylane import numpy as np

NUM_WIRES = 6


def triple_excitation_matrix(gamma):
    """The matrix representation of a triple-excitation Givens rotation.

    Args:
        - gamma (float): The angle of rotation

    Returns:
        - (np.ndarray): The matrix representation of a triple-excitation
    """

    # QHACK #

    '''The triple Givens rotation performs rotations within the two-dimensional subspace spanned by |111000> and |000111>.
    It leaves all other states unchanged. So, it's the six-qubit identity operator, except for four matrix elements related to |111000> and |000111>. 
    These elements implement the rotations and have the same values as the four matrix elements in RY(theta): cos(theta/2), sin(theta/2), 
    -sin(theta/2), and cos(theta/2). This because, abstractly, the Givens rotation does the same thing as RY(theta): it rotates within a two-dimensional state space.
    '''
    triple_excitation = np.identity(64)

    #add the matrix elements that implement rotations
    triple_excitation[7,7] = np.cos(gamma/2)
    triple_excitation[56,56] = np.cos(gamma/2)
    triple_excitation[7,56] = np.sin(gamma/2)
    triple_excitation[56,7] = -np.sin(gamma/2)    

    return triple_excitation

    # QHACK #


dev = qml.device("default.qubit", wires=6)


@qml.qnode(dev)
def circuit(angles):
    """Prepares the quantum state in the problem statement and returns qml.probs

    Args:
        - angles (list(float)): The relevant angles in the problem statement in this order:
        [alpha, beta, gamma]

    Returns:
        - (np.tensor): The probability of each computational basis state
    """

    # QHACK #

    #prepare the initial three-particle state |111000>
    qml.PauliX(wires=0)
    qml.PauliX(wires=1)
    qml.PauliX(wires=2)
    
    '''Generate the state in the problem statement.
    We can see which wires each excitation acts on by setting the angles associated with the other two rotations to zero.
    For example, by letting beta = gamma = 0, we can see that the single excitation acts on qubits 0 and 5.'''
    qml.SingleExcitation(angles[0],wires=[0,5])
    qml.DoubleExcitation(angles[1],wires=[0,1,4,5])

    qml.QubitUnitary(triple_excitation_matrix(angles[2]),wires=[0,1,2,3,4,5])

    # QHACK #

    return qml.probs(wires=range(NUM_WIRES))


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = np.array(sys.stdin.read().split(","), dtype=float)
    probs = circuit(inputs).round(6)
    print(*probs, sep=",")
