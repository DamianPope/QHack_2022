#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def switch(oracle):
    """Function that, given an oracle, returns a list of switches that work by executing a
    single circuit with a single shot. The code you write for this challenge should be completely
    contained within this function between the # QHACK # comment markers.

    Args:
        - oracle (function): oracle that simulates the behavior of the lights.

    Returns:
        - (list(int)): List with the switches that work. Example: [0,2].
    """

    dev = qml.device("default.qubit", wires=[0, 1, 2, "light"], shots=1)

    @qml.qnode(dev)
    def circuit():

        # QHACK #
        """We start solving this problem by, essentially, performing the Deutsch-Joza algorithm with the first switch as the input & the light as the output.
        We then repeat this process with the second and third switches (and the light).
        
        If a switch isn't working, then it won't change the light's state. This is equivalent to the following constant function:
            f(0) = 0
            f(1) = 0
        
        If a switch is working, then it'll flip the light qubit when the switch's state is |1>. This is equivalent to the following balanced function:
             f(0) = 0
             f(1) = 1
             
        Just as in the Deutsch-Jozsa algorithm, the constant function doesn't result in any "phase kickback" on the input qubit.
        But, the balanced function produces a phase kick of pi when the input is |1>.
        
        This leads to the following two distinct switch states:
            |0> + |1> for the CONSTANT FUNCTION (switch not working)
            |0> - |1> for the BALANCED FUNCTION (switch working)
            
        Implementing Hadamard gates on the switch qubits produces the following states:
            |0> CONSTANT FUNCTION (switch not working)
            |1> BALANCED FUNCTION( switch working)
        
        So, measuring the switches in the computational basis state (via qml.sample) produces an array that encodes which switches are working.
        Every "1" in the array corresponds to a working switch.
        Generating a list of the array indices that have the element "1" creates a list of the working switches, thus solving the problem.
        
        *Pre processing
        Initialize the switch qubits as if we’re performing the Deutsch-Jozsa algorithm"""
        for i in range(3):
            qml.Hadamard(wires=i)

        #initialize ancilla light qubit to |0> - |1>
        qml.PauliX(wires="light")
        qml.Hadamard(wires="light")

        # You are allowed to place operations before and after the oracle without any problem.
        oracle()

        """*Post processing
        Implement post-oracle unitaries on the switch qubits if we’re performing the Deutsch-Jozsa algorithm"""
        for i in range(3):
            qml.Hadamard(wires=i)

        # QHACK #

        return qml.sample(wires=range(3))

    sample = circuit()

    # QHACK #

    

    # Process the received sample and return the requested list.

    workingSwitches=[]

    for i in range(3):
        if sample[i] == 1:
            workingSwitches.append(i) 

    return workingSwitches

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    def oracle():
        for i in numbers:
            qml.CNOT(wires=[i, "light"])

    output = switch(oracle)
    print(*output, sep=",")
