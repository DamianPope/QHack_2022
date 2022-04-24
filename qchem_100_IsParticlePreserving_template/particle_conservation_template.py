#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


def binary_list(m, n):
    """Converts number m to binary encoded on a list of length n

    Args:
        - m (int): Number to convert to binary
        - n (int): Number of wires in the circuit

    Returns:
        - (list(int)): Binary stored as a list of length n
    """

    arr = []
    # QHACK #
    
    #Starting with the most significant bit, calculate value of each bit in the binary representation of m.
    #Do this by calculating m/(2^p), where p = n-1, n-2 ... 0, and ignoring the remainder (i.e., anything after the decimal point)
    
    for i in range(n):
        arr.append(int(np.trunc(m/(2**(n-1-i)))))
   
        #Subtract the value of the bit that we've just calculated from m before calculating m/(2^p) again
        m -= arr[i]*2**(n-1-i)

    # QHACK #
        
    return arr


def basis_states(n):
    """Given a number n, returns a list of all binary_list(m,n) for m < 2**n, thus providing all basis states
         for a circuit of n wires

    Args:
        - n(int): integer representing the number of wires in the circuit

    Returns:
        - (list(list(int))): list of basis states represented as lists of 0s and 1s.
    """

    arr = []

    # QHACK #

    for i in range(2**n):
        arr.append(binary_list(i,n))

    # QHACK #

    return arr


def is_particle_preserving(circuit, n):
    """Given a circuit and its number of wires n, returns 1 if it preserves the number of particles, and 0 if it does not

    Args:
        - circuit (qml.QNode): A QNode that has a state such as [0,0,1,0] as an input and outputs the final state after performing
        quantum operation
        - n (int): the number of wires of circuit

    Returns:
        - (bool): True / False according to whether the input circuit preserves the number of particles or not
    """

    # QHACK #

    #Bool variable that tracks whether circuit is particle preserving (True) or not (False)
    preservingFlag = True

    arr = basis_states(n)

    #For each computational basis state as the input, test to see if the circuit is particle preserving
    for i in range(len(arr)):        
          
        #calculate number of 1's in input state
        initialBinaryString = binary_list(i,n)
        initial_one_count = initialBinaryString.count(1)
        
        
        #execute circuit
        state_array = circuit(arr[i])
        
        
        #Calculate the number of 1's in every nonzero element in the output statevector        
        for j in range(len(state_array)):
            if np.abs(state_array[j]>=0.00001):
                #calculate the binary string associated with j
                binaryTestString = binary_list(j,n)
        
                one_count =  binaryTestString.count(1)

                #If the number of 1's in an output state is different to the number of 1's in the input state, then circuit isn't particle preserving.
                if one_count != initial_one_count: 
                     preservingFlag = False                
                     break
    
        if preservingFlag == False:
            break
    
    return preservingFlag
    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(";")
    gate_list = []
    wire_list = []
    param_list = []
    i = 1

    while i < len(inputs):
        gate_obj = getattr(qml, str(inputs[i]))
        gate_wires = gate_obj.num_wires
        input_wires = list(map(int, str(inputs[i + 1]).split(",")))
        gate_list.append(str(inputs[i]))
        wire_list.append(input_wires)
        if "non_parametric_ops" not in gate_obj.__module__.split("."):
            input_params = list(map(float, str(inputs[i + 2]).split(",")))
            param_list.append(input_params)
            i += 1
        i += 2

    wire_list = np.array(wire_list, dtype=object)
    param_list = np.array(param_list, dtype=object)

    n = int(inputs[0])
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circ(gate_list, wire_list, param_list, state):
        qml.BasisState(np.array(state), wires=range(n))
        j = 0
        for i in range(len(gate_list)):
            gate = getattr(qml, str(gate_list[i]))
            if "non_parametric_ops" not in gate.__module__.split("."):
                gate(*param_list[j], wires=[int(w) for w in wire_list[i]])
                j += 1
            else:
                gate(wires=[int(w) for w in wire_list[i]])
        return qml.state()

    def circuit(state):
        return circ(gate_list, wire_list, param_list, state)

    output = is_particle_preserving(circuit, n)

    print(output)
