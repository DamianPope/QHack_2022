#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def qRAM(thetas):
    """Function that generates the superposition state explained above given the thetas angles.

    Args:
        - thetas (list(float)): list of angles to apply in the rotations.

    Returns:
        - (list(complex)): final state.
    """

    # QHACK #

    # Use this space to create auxiliary functions if you need it.

    # QHACK #

    dev = qml.device("default.qubit", wires=range(4))

    @qml.qnode(dev)
    def circuit():

        # QHACK #

        # Create your circuit: the first three qubits will refer to the index, the fourth to the RY rotation.
        
        #Create an equal superposition of all eight basis states of the first three qubits.
        for i in range(3):
            qml.Hadamard(wires=i)

        binaryStrings=['000','001','010','011','100','101','110','111']
        
        for i in range(8):
            #create a tensor that represents a rotation about Y axis by the angle thetas[i]
            U=qml.RY.compute_matrix(thetas[i])    
           
            #when the first three qubits are in the state |binaryStrings[i]>, implement the operation U(thetas[i]) on the 4th qubit    
            qml.ControlledQubitUnitary(U, control_wires=[0, 1, 2], wires=3, control_values=binaryStrings[i])

        # QHACK #

        return qml.state()

    return circuit()


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    thetas = np.array(inputs, dtype=float)

    output = qRAM(thetas)
    output = [float(i.real.round(6)) for i in output]
    print(*output, sep=",")
