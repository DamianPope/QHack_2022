import sys
import pennylane as qml
from pennylane import numpy as np
from pennylane import hf

import math


def ground_state_VQE(H):
    """Perform VQE to find the ground state of the H2 Hamiltonian.

    Args:
        - H (qml.Hamiltonian): The Hydrogen (H2) Hamiltonian

    Returns:
        - (float): The ground state energy
        - (np.ndarray): The ground state calculated through your optimization routine
    """

    # QHACK #
    num_wires=len(H.wires)
    
    dev = qml.device("default.qubit", wires=num_wires)

    def circuit(theta,localNumWires):
        #Start with the Hartree-Fock (HF) state |1100> 
        qml.BasisState(np.array([1,1,0,0]), wires=range(localNumWires))
        
        #Evolve state to a superposition of the HF state & a state that's a double excitation from it 
        qml.DoubleExcitation(theta, wires=[0, 1, 2, 3])
    
    @qml.qnode(dev)
    def cost_fn(param):     
       circuit(param,num_wires) 
       return qml.expval(H)
      
    opt  = qml.GradientDescentOptimizer(stepsize =0.4)
    theta = np.array(0.0,requires_grad=True)
    
    tolerance=5e-06
    epochs = 500

    for i in range(epochs):
        theta,previous_E = opt.step_and_cost(cost_fn,theta)
        E = cost_fn(theta)

        delta = np.abs(previous_E - E)

        if delta < tolerance:
            break

    #return the ground-state energy & an array that represents the ground state in the computational basis    
    return E,np.array([0,0,0,-math.sin(theta/2),0,0,0,0,0,0,0,0,math.cos(theta/2),0,0,0])
    # QHACK #


def create_H1(ground_state, beta, H):
    """Create the H1 matrix, then use `qml.Hermitian(matrix)` to return an observable-form of H1.

    Args:
        - ground_state (np.ndarray): from the ground state VQE calculation
        - beta (float): the prefactor for the ground state projector term
        - H (qml.Hamiltonian): the result of hf.generate_hamiltonian(mol)()

    Returns:
        - (qml.Observable): The result of qml.Hermitian(H1_matrix)
    """

    # QHACK #    
    #create a column vector that represents the ground state as a ket
    groundStateKet = np.transpose(np.array([ground_state]))

    #create the projector onto the ground state by using matrix multiplication with the ket |grnd state> & the bar <grnd state|
    groundStateProjector=np.matmul(groundStateKet,np.array([ground_state]))
   
    #get the matrix form of the Hamiltonian H. Note that sparse_hamiltonian returns a sparse matrix representation of H.
    #This representation only includes nonzero terms.
    Hmat = qml.utils.sparse_hamiltonian(H).real
    Harray = Hmat.toarray()
    
    #create new Hamiltonian by combining H, beta, and the grnd state projector
    H1_matrix = groundStateProjector*beta + Harray
    
    return qml.Hermitian(H1_matrix,wires=[0,1,2,3])
    # QHACK #


def excited_state_VQE(H1):
    """Perform VQE using the "excited state" Hamiltonian.

    Args:
        - H1 (qml.Observable): result of create_H1

    Returns:
        - (float): The excited state energy
    """

    # QHACK #
    dev_H1 = qml.device("default.qubit", wires=[0,1,2,3])
    num_wires=len(H1.wires)
    
    def circuit_H1(theta,num_wires):
        #start with the state |0101>
        qml.BasisState(np.array([0,1,0,1]), wires=range(num_wires))
        
        #perform a single excitation that can take |0101> to |0011> by "exciting" qubit 2 to qubit 1
        qml.SingleExcitation(theta, wires=[1, 2])
            
    @qml.qnode(dev_H1)
    def cost_fn_H1(param):
       circuit_H1(param,num_wires)
       return qml.expval(H1)

    opt = qml.GradientDescentOptimizer(stepsize = 0.01)
    theta_1 = np.array(0.5,requires_grad=True)

    tolerance = 5e-06
    epochs = 500

    for n in range(epochs):
        theta_1,previous_E = opt.step_and_cost(cost_fn_H1,theta_1)
        E = cost_fn_H1(theta_1)
    
        conv = np.abs(previous_E - E)

        if conv < tolerance:
            break

    return E
    # QHACK #


if __name__ == "__main__":
    coord = float(sys.stdin.read())
    symbols = ["H", "H"]
    geometry = np.array([[0.0, 0.0, -coord], [0.0, 0.0, coord]], requires_grad=False)
    mol = hf.Molecule(symbols, geometry)

    H = hf.generate_hamiltonian(mol)()
    E0, ground_state = ground_state_VQE(H)

    beta = 15.0
    H1 = create_H1(ground_state, beta, H)
    E1 = excited_state_VQE(H1)

    answer = [np.real(E0), E1]
    print(*answer, sep=",")
