#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


dev = qml.device("default.qubit", wires=[0, 1, "sol"], shots=1)


def find_the_car(oracle):
    """Function which, given an oracle, returns which door that the car is behind.

    Args:
        - oracle (function): function that will act as an oracle. The first two qubits (0,1)
        will refer to the door and the third ("sol") to the answer.

    Returns:
        - (int): 0, 1, 2, or 3. The door that the car is behind.
    """

    @qml.qnode(dev)
    def circuit1():
        # QHACK #
        
        """The door with the car behind it is found as follows:
            1. Effectively, run Deutsch's algorithm with the 2nd qubit as the input & the sol qubit as the output. Do this by preparing the state:
                |0> (|0> + |1>) (|0> - |1>)
            
            Case A: If the second qubit is 1 by the end of circuit, then 00 and 01 have different outputs. So, one of them must be the solution. 
            (As only the solution produces the output of 1.) 
            
            Case B: If the second qubit is 0 by the end of circuit, then 00 and 01 produce the same output. 
            So, neither of them is the solution.
            
           2. Essentially, run Deutsch's algorithm again but with the 1st qubit as the input & the initial state (|0> + |1>) |0> (|0> - |1>).
            CASE A: If the first qubit is 1 at the end of the circuit, then then 00 and 10 have different outputs. So, one of them must be the solution. 
            CASE B: If the first qubit is 0 by the end of circuit, then 00 and 10 produce the same output. So, neither of them is the solution.
            
            3. Use logic to process the outputs of the circuits and determine where the car is.
        """
        
        #prepare the input state of |00> + |01>
        qml.Hadamard(wires=1)

        #prepare the sol qubit (3rd qubit) in the state |0> - |1>
        qml.PauliX(wires="sol")
        qml.Hadamard(wires="sol")
        
        oracle()

        #apply H gate to 2nd qubit
        qml.Hadamard(wires=1)

        # QHACK #
        return qml.sample()

    @qml.qnode(dev)
    def circuit2():
        # QHACK #
       
        #prepare the input state of |00> + |10>
        qml.Hadamard(wires=0)

        #prepare the sol qubit (3rd qubit) in the state |0> - |1>
        qml.PauliX(wires="sol")
        qml.Hadamard(wires="sol")
            
        oracle() 
        
        #apply H gate to 1st qubit
        qml.Hadamard(wires=0)
        
        # QHACK #
        return qml.sample()

    sol1 = circuit1()
    sol2 = circuit2()

    # QHACK #    
    
    # process sol1 and sol2 to determine which door the car is behind.
    
    if sol1[1] == 1 and sol2[0]==0:
        return 1

    if sol1[1] == 1 and sol2[0]==1:
        return 0
        
    if sol1[1] == 0 and sol2[0]==0:
        return 3

    if sol1[1] == 0 and sol2[0]==1:
        return 2
    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    def oracle():
        
        
        if numbers[0] == 1:
            qml.PauliX(wires=0)
        if numbers[1] == 1:
            qml.PauliX(wires=1)
        qml.Toffoli(wires=[0, 1, "sol"])
        if numbers[0] == 1:
            qml.PauliX(wires=0)
        if numbers[1] == 1:
            qml.PauliX(wires=1)

    output = find_the_car(oracle)
    print(f"{output}")
