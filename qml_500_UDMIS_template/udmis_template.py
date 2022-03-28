import sys
import pennylane as qml
from pennylane import numpy as np


def hamiltonian_coeffs_and_obs(graph):
    """Creates an ordered list of coefficients and observables used to construct
    the UDMIS Hamiltonian.

    Args:
        - graph (list((float, float))): A list of x,y coordinates. e.g. graph = [(1.0, 1.1), (4.5, 3.1)]

    Returns:
        - coeffs (list): List of coefficients for elementary parts of the UDMIS Hamiltonian
        - obs (list(qml.ops)): List of qml.ops
    """

    num_vertices = len(graph)
    E, num_edges = edges(graph)
    u = 1.35
    obs = []
    coeffs = []

    # QHACK #

    # create the Hamiltonian coeffs and obs variables here

    #
    #create all the terms in the obs list
    #
    
    #create the constant numerical obs term 
    obs_constant_term = [qml.Identity(wires=0)]
    
    #initialize list that stores all the obs elements associated with just one qubit
    obs_single_qubit_terms=[]
    
    for i in range(num_vertices):
        obs_single_qubit_terms.append(qml.PauliZ(i))

    coeffs_constant_term=[0.0]

    #initialize list that stores the coeffs of Z_0, Z_1 ... Z_(num_vertices-1)
    coeffs_one_qubit_terms=[]

    for i in range(num_vertices):
        coeffs_one_qubit_terms.append(0.0)

    """Create a list of all the two-qubit interactions in the Hamiltonian that add elements to obs.
    Do this by going through all the off-diagonal elements in the top right half of E.
    For each non-zero element, create a PauliZ-PauliZ coupling between the two indices of the element."""
    obs_two_qubit_terms=[]
    
    for i in range(np.size(E,0)):
        for j in range(i+1,np.size(E,0)):
            if E[i,j]==1:
                #vertices i & j are within one unit of distance. So, add the associated two-qubit terms to obs.
                obs_two_qubit_terms.append(qml.PauliZ(i)@qml.PauliZ(j))
    
                #add to the three terms below in the coeffs list that come from three of the four terms in u*((Z_i+1)/2)((Z_j+1)/2)
                coeffs_constant_term[0]+=u/4
    
                coeffs_one_qubit_terms[i]+=u/4
                coeffs_one_qubit_terms[j]+=u/4    

    #
    #define remaining coeffs
    #

    #contribution from first term in Hamiltonian
    coeffs_constant_term[0]-=num_vertices/2

    #coeffs of the two-qubit terms in Hamiltonian
    coeffs_two_qubit_terms=[]
    
    for i in range(len(obs_two_qubit_terms)):
        coeffs_two_qubit_terms.append(u/4)

    #coeffs for one-qubit terms: -1/2 contribution from the first half of the Hamiltonian
    for i in range(num_vertices):
        coeffs_one_qubit_terms[i]-=1/2 

    #combine all the parts of obs & coeffs
    obs = obs_constant_term + obs_single_qubit_terms + obs_two_qubit_terms
    coeffs=coeffs_constant_term + coeffs_one_qubit_terms + coeffs_two_qubit_terms
    # QHACK #

    return coeffs, obs


def edges(graph):
    """Creates a matrix of bools that are interpreted as the existence/non-existence (True/False)
    of edges between vertices (i,j).

    Args:
        - graph (list((float, float))): A list of x,y coordinates. e.g. graph = [(1.0, 1.1), (4.5, 3.1)]

    Returns:
        - num_edges (int): The total number of edges in the graph
        - E (np.ndarray): A Matrix of edges
    """

    # DO NOT MODIFY anything in this code block
    num_vertices = len(graph)
    E = np.zeros((num_vertices, num_vertices), dtype=bool)
    
    for vertex_i in range(num_vertices - 1):
        xi, yi = graph[vertex_i]  # coordinates

        for vertex_j in range(vertex_i + 1, num_vertices):
            xj, yj = graph[vertex_j]  # coordinates
            dij = np.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)
            E[vertex_i, vertex_j] = 1 if dij <= 1.0 else 0

    return E, np.sum(E, axis=(0, 1))


def variational_circuit(params, num_vertices):
    """A variational circuit.

    Args:
        - params (np.ndarray): your variational parameters
        - num_vertices (int): The number of vertices in the graph. Also used for number of wires.
    """

    # QHACK #

    # create your variational circuit here

    """Rotate each qubit about Y axis by an angle equal to the value of one of the theta parameters.
    
    As the Hamiltonian maps to the UDMIS problem, the ground state is a computational basis state. 
    This is because it corresponds to the bit string that encodes the solution to the UDMIS problem.
    So, we only need to explore fully separable quantum states during the learning process.
    So, the choice of fully separable parameterized states below is sufficient."""
    for i in range(0,num_vertices):
             qml.RY(params[i],wires=i)
         
    # QHACK #


def train_circuit(num_vertices, H):
    """Trains a quantum circuit to learn the ground state of the UDMIS Hamiltonian.

    Args:
        - num_vertices (int): The number of vertices/wires in the graph
        - H (qml.Hamiltonian): The result of qml.Hamiltonian(coeffs, obs)

    Returns:
        - E / num_vertices (float): The ground state energy density.
    """

    dev = qml.device("default.qubit", wires=num_vertices)

    @qml.qnode(dev)
    def cost(params):
        """The energy expectation value of a Hamiltonian"""
        variational_circuit(params, num_vertices)
        return qml.expval(H)

    # QHACK #

    # define your trainable parameters and optimizer here
    # change the number of training iterations, `epochs`, if you want to
    # just be aware of the 80s time limit!

    opt = qml.GradientDescentOptimizer(stepsize=0.4)
    
    #Create an ansatz of |000...0> which is equivalent to |n_0=1, n_1=1, ... n_num_vertices = 1>
    #I.e., all the vertices are occupied    
    params = np.zeros(num_vertices, requires_grad=True)

    #initialize trainable parameters    
    for i in range(num_vertices):    
        params[i]=3.14159/2

    #initialize E, the system's energy
    E = cost(params)

    epochs = 500

    # QHACK #

    for i in range(epochs):
        params, E = opt.step_and_cost(cost, params)

    return E / float(num_vertices)


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = np.array(sys.stdin.read().split(","), dtype=float, requires_grad=False)
    num_vertices = int(len(inputs) / 2)
    x = inputs[:num_vertices]
    y = inputs[num_vertices:]
    graph = []
    for n in range(num_vertices):
        graph.append((x[n].item(), y[n].item()))

    coeffs, obs = hamiltonian_coeffs_and_obs(graph)
    H = qml.Hamiltonian(coeffs, obs)

    energy_density = train_circuit(num_vertices, H)
    print(f"{energy_density:.6f}")
