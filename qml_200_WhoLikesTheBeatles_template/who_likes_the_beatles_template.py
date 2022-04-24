#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def distance(A, B):
    """Function that returns the distance between two vectors.

    Args:
        - A (list[int]): person's information: [age, minutes spent watching TV].
        - B (list[int]): person's information: [age, minutes spent watching TV].

    Returns:
        - (float): distance between the two feature vectors.
    """

    # QHACK #

    # The Swap test is a method that allows you to calculate |<A|B>|^2 , you could use it to help you.
    # The qml.AmplitudeEmbedding operator could help you too.

    # dev = qml.device("default.qubit", ...
    # @qml.qnode(dev)

    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit(A,B):
        
        #create the circuit for the SWAP test: https://en.wikipedia.org/wiki/Swap_test    
        qml.Hadamard(wires=0)
        
        #encode information about each person into a qubit
        #A:
        phi = np.arctan(A[1]/A[0])
        
        #Multiply phi by 2 to counteract the effect of the factor of 1/2 in the rotation. I.e., RY(phi)|0> = cos(phi/2) |0> + sin(phi/2) |1>
        #So, when we multiply phi by 2, we get |psi> = cos(phi) |0> + sin(phi) |1>, as desired.
        qml.RY(2*phi,wires=1)
        
        #B:
        phi = np.arctan(B[1]/B[0])
        qml.RY(2*phi,wires=2)    
        
        qml.CSWAP(wires=[0,1,2]) 
    
        qml.Hadamard(wires=0)
    
        return qml.probs(wires=0)
 
    x = circuit(A,B)[1]

    #return sqrt(2*(1-|<A|B>|)), where |<A|B>| = sqrt(1-2*x), where x is the probability of qubit 0 being 1.  
    return np.sqrt(2*(1-np.sqrt(-2*x+1)))    

    # QHACK #


def predict(dataset, new, k):
    """Function that given a dataset, determines if a new person do like Beatles or not.

    Args:
        - dataset (list): List with the age, minutes that different people watch TV, and if they like Beatles.
        - new (list(int)): Age and TV minutes of the person we want to classify.
        - k (int): number of nearby neighbors to be taken into account.

    Returns:
        - (str): "YES" if they like Beatles, "NO" otherwise.
    """

    # DO NOT MODIFY anything in this code block

    def k_nearest_classes():
        """Function that returns a list of k near neighbors."""
        distances = []
          
        for data in dataset:
            distances.append(distance(data[0], new))
        nearest = []
        for _ in range(k):
            indx = np.argmin(distances)
            nearest.append(indx)
            distances[indx] += 2

        return [dataset[i][1] for i in nearest]

    output = k_nearest_classes()

    return (
        "YES" if len([i for i in output if i == "YES"]) > len(output) / 2 else "NO",
        float(distance(dataset[0][0], new)),
    )


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    dataset = []
    new = [int(inputs[0]), int(inputs[1])]
    k = int(inputs[2])
    for i in range(3, len(inputs), 3):
        dataset.append([[int(inputs[i + 0]), int(inputs[i + 1])], str(inputs[i + 2])])

    output = predict(dataset, new, k)
    sol = 0 if output[0] == "YES" else 1
    print(f"{sol},{output[1]}")
