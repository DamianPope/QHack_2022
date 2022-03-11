#! /usr/bin/python3

import sys
#from pennylane import numpy as np
import pennylane as qml

graph = {
    0: [1],
    1: [0, 2, 3, 4],
    2: [1],
    3: [1],
    4: [1, 5, 7, 8],
    5: [4, 6],
    6: [5, 7],
    7: [4, 6],
    8: [4],
}

#initialize global variable that counts minimum number of swap gates required to connect two qubits
minNumSwaps=0


def n_swaps(cnot):
    """Count the minimum number of swaps needed to create the equivalent CNOT.

    Args:
        - cnot (qml.Operation): A CNOT gate that needs to be implemented on the hardware
        You can find out the wires on which an operator works by asking for the 'wires' attribute: 'cnot.wires'

    Returns:
        - (int): minimum number of swaps
    """

    # QHACK #

    #controlList is a *list* of all the qubits we need to check to see if they're connected to target qubit
    #the outer set of square parentheses converts cnot.wires[0] from an integer to a list
    controlList=[cnot.wires[0]]
    target=cnot.wires[1]    
  
    global minNumSwaps
    
    #check to see if any qubits in the control list are connected to target qubit
    testForConnection(controlList,target)

    return minNumSwaps

#function that tests if a qubit is connected to target qubit        
def testForConnection(localControlList,localTarget):
    newLocalControlList=[]
          
    #loop through all qubits in localControlList
    for i in range(len(localControlList)):
        for j in range(len(graph[localControlList[i]])):        
            
            #test to see if a qubit in list of control qubits is same as target qubit
            if graph[localControlList[i]][j]==localTarget:
                return
                
            #build up a list of qubits that are connected to qubits in localControlList 
            newLocalControlList.append(graph[localControlList[i]][j])
                
    #if we reach here, we've looked through all the qubits in localControlList & none are directly connected to target node
    #Repeat search process for at least one more iteration
    
    global minNumSwaps
    
    #increment minimum number of swaps by two as we need to swap two qubit states (+1) & then swap them back (+1) 
    minNumSwaps+=2
    
    #test to see if any of qubits in new controlList are directly connected to target qubit
    testForConnection(newLocalControlList,localTarget)          
    
    return    
    # QHACK #
    


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    output = n_swaps(qml.CNOT(wires=[int(i) for i in inputs]))
    print(f"{output}")
