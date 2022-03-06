#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np

dev = qml.device("default.qubit", wires=3)


def my_finite_diff_grad(params):
    """Function that returns the gradients of the cost function (defined below) with respect 
    to all parameters in params.

    Args:
        - params (np.ndarray): The parameters needed to create the variational circuit.

    Returns:
        - gradients (np.ndarray): the gradient w.r.t. each parameter
    """

    gradients = np.zeros([len(params)])
  
    for i in range(len(params)):

        # QHACK # 

        #delta is the amount of change to each of the six parameters
        delta = 0.010000

        #create two arrays to store changed parameters in, one for +delta/2 and one for -delta/2
        tmpParams = np.copy(params)
        tmpParamsTwo = np.copy(params)    
        
        #change value of i-th parameter
        tmpParamsTwo[i]+=delta
        tmpParams[i]-=delta
        
        #calculate gradient with respect to i-th parameter using finite difference method
        gradients[i]=(cost(tmpParamsTwo)-cost(tmpParams))/(2.0*delta)
        # QHACK #

    return gradients


def variational_circuit(params):
    """A layered variational circuit. The first layer comprises of x, y, and z rotations on wires
    0, 1, and 2, respectively. The second layer is a ring of CNOT gates. The final layer comprises 
    of x, y, and z rotations on wires 0, 1, and 2, respectively.
    """

    # DO NOT MODIFY anything in this code block
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.RZ(params[2], wires=2)

    qml.broadcast(qml.CNOT, wires=[0, 1, 2], pattern="ring")

    qml.RX(params[3], wires=0)
    qml.RY(params[4], wires=1)
    qml.RZ(params[5], wires=2)

    qml.broadcast(qml.CNOT, wires=[0, 1, 2], pattern="ring")


@qml.qnode(dev)
def cost(params):
    """A QNode that pairs the variational_circuit with an expectation value measurement.

    Args:
        - params (np.ndarray): Variational circuit parameters

    Returns:
        - (float): qml.expval(qml.PauliY(0) @ qml.PauliZ(2))
    """

    # DO NOT MODIFY anything in this code block
    variational_circuit(params)
    return qml.expval(qml.PauliY(0) @ qml.PauliZ(2))


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    params = np.array(sys.stdin.read().split(","), dtype=float)
    output = my_finite_diff_grad(params)
    print(*output, sep=",")
