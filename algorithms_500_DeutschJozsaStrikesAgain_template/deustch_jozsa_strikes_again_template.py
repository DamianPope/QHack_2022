#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml

"""
The general approach to solving this problem is as follows:
    implement Deutsch-Jozsa algorithm with oracle 1
    transfer result from qubits 0 & 1 to qubit 2 (using MultiControlledX)
    transfer result to qubit 3 by rotating it by Pi/2 about the Y axis if qubit 2 is |1>
    "reset" qubits 0, 1, and 2 by performing the inverse of some of the operations implemented on them (including oracle 1)
    repeat the process for oracles 2, 3, and 4
    
    At this point, there two possibilities:
        1. all four functions are constant: qubit 3 has been rotated by Pi/2 four times & has returned to |0>
        2. two functions are balanced & two are constant: qubit 3 has been rotated two times & taken to |1>
        
    Measure qubit 3 and return "4 same" if it's |0> and "2 and 2" otherwise    
"""

def deutsch_jozsa(fs):
    """Function that determines whether four given functions are all of the same type or not.

    Args:
        - fs (list(function)): A list of 4 quantum functions. Each of them will accept a 'wires' parameter.
        The first two wires refer to the input and the third to the output of the function.

    Returns:
        - (str) : "4 same" or "2 and 2"
    """



    # QHACK #
    output=circuit(fs)
    
    #if state of qubit 3 is close to being |0>, then all four oracles are the same
    if output[0]>0.99:
        return "4 same"
    
    #two functions are balanced & two are constant
    else:
        return "2 and 2"    
    
dev = qml.device("default.qubit", wires=4)

@qml.qnode(dev)
def circuit(fs):

    #
    #Prepare qubits 0, 1, and 2 according to the Deutsch-Jozsa algorithm
    #
    
    #perform Hadamards on two input qubits
    qml.Hadamard(wires=0)
    qml.Hadamard(wires=1)
    
    #prepare output qubit (i.e., qubit 2) in |1> & then perform an H gate
    qml.PauliX(wires=2)
    qml.Hadamard(wires=2)

    """
    The code below performs the following sequence:
    1. implements Deutsch-Jozsa algorithm with oracle 1 (i.e., f1), 
    2. stores output in state of qubit 2 (|0> = balanced function, |1> = constant function)
    3. rotates qubit 3 if qubit 2 is |1>
    4. returns qubits 0, 1, & 2 to their state prior to implementing f1
    5. repeats steps 1, 2, 3, and 4 for oracles f2, f3, and f4
    """

    #implement first oracle
    implement_oracle_and_next_gates(f1)
    reverseUnitaries(f1)
    
    #implement second oracle
    implement_oracle_and_next_gates(f2)
    reverseUnitaries(f2)

    #implement third oracle
    implement_oracle_and_next_gates(f3)
    reverseUnitaries(f3)
    
    #implement fourth oracle
    implement_oracle_and_next_gates(f4)

    #measure state of qubit 3
    return qml.probs(wires=3)
 
def implement_oracle_and_next_gates(oracle):
    #implement desired oracle, i.e., f1, f2, f3, or f4
    oracle(wires=[0,1,2])

    #perform second set of Hadamards on input qubits
    qml.Hadamard(wires=0)
    qml.Hadamard(wires=1)

    """perform rotation on output qubit to take it to |0>
    This makes sure that it's prepared in the correct state for the MultiControlledX operation
    """
    qml.RY(3.14159/2,wires=2)

    """result of Deutsch-Jozsa algorithm is encoded in first two qubits. Transfer it to the output qubit (qubit 2)
    After this operation, the output qubit is such that:
        |1> --> constant function
        |0> --> balanced function"""
    qml.MultiControlledX(control_wires=[0,1], wires=[2], control_values="00")
    
    """perform controlled Pi/2 rotation on qubit 3
    This rotation is performed only if the oracle that was just implemented has a constant function"""
    qml.CRY(3.14159/2,wires=[2,3])        
    return

"""reverse MultiControlledX, H gates on qubits 0 & 1, RY on qubit 2, and oracle to "reset" first three qubits 
and prepare them for the next oracle"""
def reverseUnitaries(oracle):
    qml.adjoint(qml.MultiControlledX)(control_wires=[0,1], wires=[2], control_values="00")
    
    qml.Hadamard(wires=0)
    qml.Hadamard(wires=1)
    qml.RY(-3.14159/2,wires=2)

    qml.adjoint(oracle)(wires=[0,1,2])

    return

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this co de block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    # Definition of the four oracles we will work with.

    def f1(wires):
        qml.CNOT(wires=[wires[numbers[0]], wires[2]])
        qml.CNOT(wires=[wires[numbers[1]], wires[2]])

    def f2(wires):
        qml.CNOT(wires=[wires[numbers[2]], wires[2]])
        qml.CNOT(wires=[wires[numbers[3]], wires[2]])

    def f3(wires):
        qml.CNOT(wires=[wires[numbers[4]], wires[2]])
        qml.CNOT(wires=[wires[numbers[5]], wires[2]])
        qml.PauliX(wires=wires[2])

    def f4(wires):
        qml.CNOT(wires=[wires[numbers[6]], wires[2]])
        qml.CNOT(wires=[wires[numbers[7]], wires[2]])
        qml.PauliX(wires=wires[2])

    output = deutsch_jozsa([f1, f2, f3, f4])
    print(f"{output}")
