import sys
import pennylane as qml
from pennylane import numpy as np
import pennylane.optimize as optimize


DATA_SIZE = 250


def square_loss(labels, predictions):
    """Computes the standard square loss between model predictions and true labels.

    Args:
        - labels (list(int)): True labels (1/-1 for the ordered/disordered phases)
        - predictions (list(int)): Model predictions (1/-1 for the ordered/disordered phases)

    Returns:
        - loss (float): the square loss
    """

    loss = 0
    for l, p in zip(labels, predictions):
        loss = loss + (l - p) ** 2

    loss = loss / len(labels)
    return loss


def accuracy(labels, predictions):
    """Computes the accuracy of the model's predictions against the true labels.

    Args:
        - labels (list(int)): True labels (1/-1 for the ordered/disordered phases)
        - predictions (list(int)): Model predictions (1/-1 for the ordered/disordered phases)

    Returns:
        - acc (float): The accuracy.
    """

    acc = 0
    for l, p in zip(labels, predictions):
        if abs(l - p) < 1e-5:
            acc = acc + 1
    acc = acc / len(labels)

    return acc


def classify_ising_data(ising_configs, labels):
    """Learn the phases of the classical Ising model.

    Args:
        - ising_configs (np.ndarray): 250 rows of binary (0 and 1) Ising model configurations
        - labels (np.ndarray): 250 rows of labels (1 or -1)

    Returns:
        - predictions (list(int)): Your final model predictions

    Feel free to add any other functions than `cost` and `circuit` within the "# QHACK #" markers 
    that you might need.
    """

    # QHACK #
    num_wires = ising_configs.shape[1] 
    dev = qml.device("default.qubit", wires=num_wires) 


    #define the structure of a single layer within the quantum neural network; W is a matrix that encodes all the weights in a single layer
    def layer(W):
        qml.Rot(W[0, 0], W[0, 1], W[0, 2], wires=0)
        qml.Rot(W[1, 0], W[1, 1], W[1, 2], wires=1)
        qml.Rot(W[2, 0], W[2, 1], W[2, 2], wires=2)
        qml.Rot(W[3, 0], W[3, 1], W[3, 2], wires=3)
    
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[3, 0])


    # Define a variational circuit below with your needed arguments and return something meaningful
    @qml.qnode(dev)
    def circuit(spins,weights):
        
        """
        Args:
           -spins : array of the values of the four spins in a single piece of data
           -weights : matrix containing all the neural network weights for every layer
        """       
    
        #prepare initial state
        qml.BasisState(spins, wires=[0, 1, 2, 3])                

        #Execute all the layers of the network. Note that len(weights) = number of layers
        for W in weights:
            layer(W)

        return qml.expval(qml.PauliZ(0))


    #define the output of the classifier for a single set of four input spins (i.e., a single piece of data)
    def variational_classifier(weights, bias, spins):
        return circuit(spins,weights) + bias

    # Define a cost function below with your needed arguments
    def cost(weights, bias, ising_configs, Y):

        # QHACK #
        
        """
        Args:
            -ising_configs = array of all the sets of spin configurations
            -Y = array of all the phases, disordered (-1) or ordered (+1)
        """
        
        # Insert an expression for your model predictions here
        #Note that this is the prediction differs slightly from our actual prediction as it doesn't include np.sign()
        #However, the optimization process works well with this definition but doesn't work well when np.sign() is included
        predictions =  [variational_classifier(weights, bias, x) for x in ising_configs]

        # QHACK #

        return square_loss(Y, predictions) # DO NOT MODIFY this line

    # optimize your circuit here

    #Set the seed for generating random numbers. This is helpful as it results in outputting the same result when the program is run multiple times
    np.random.seed(0)
    
    num_layers = 2

    #Generate initial random values for the weights in the neural network.
    #weights_init is a 3-D tensor of dimensions num_layers x num_wires x 3
    #The '3' argument denotes the three weights for each qubit (for each layer)
    weights_init = 0.15 * np.random.randn(num_layers, num_wires, 3, requires_grad=True)
    
    #initialize value of bias parameter
    bias_init = np.array(0.0, requires_grad=True)
    

    #Use a gradient descent optimizer with Neseterov momentum. The argument 0.5 is the step size. The momentum parameter is 0.9 by default.    
    opt = optimize.NesterovMomentumOptimizer(0.5)
 
    batch_size = 5
      
    weights = weights_init
    bias = bias_init

    #Maximum number of times that we go through entire data set while optimizing
    epochs = 5

    #Boolean flag that tells us if the accuracy has reached 0.9 and so we can stop     
    breakFlag=False
        
    for i in range(epochs):
        for j in range(int(DATA_SIZE/batch_size)):
            batch_index_array=np.random.randint(0, DATA_SIZE, (batch_size,))                
            
            X_batch = ising_configs[batch_index_array]
            Y_batch = labels[batch_index_array]
      
            weights, bias, _, _ = opt.step(cost, weights, bias, X_batch, Y_batch)
           
           
            #Use the current weights to generate predictions for the entire data set of 250 data points
            #The function qml.expval(PauliX) returns a float in the interval [-1,+1] but the desired answer is either -1 or +1
            #So, convert the float to +/-1 using numpy.sign()
            predictions = [int(np.sign(variational_classifier(weights, bias, x))) for x in ising_configs]
            
            #Test accuracy of the predictions. acc needs to be >= 0.9 in order to successfully solve the problem
            acc = accuracy(labels, predictions)        

            #Include this line if you want to see how the optimization process progresses
            #print("accuracy=",acc," |epoch=",i,"|j=",j)
             
            if acc >= 0.9:
                breakFlag=True
                break
    
        #if accuracy >= 0.9, exit epochs loop
        if breakFlag:
            break            
    
    # QHACK #

    return predictions


if __name__ == "__main__":
    inputs = np.array(
        sys.stdin.read().split(","), dtype=int, requires_grad=False
    ).reshape(DATA_SIZE, -1)
    ising_configs = inputs[:, :-1]
    labels = inputs[:, -1]
    predictions = classify_ising_data(ising_configs, labels)
    print(*predictions, sep=",")
