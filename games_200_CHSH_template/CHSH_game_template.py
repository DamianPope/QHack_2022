#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


dev = qml.device("default.qubit", wires=2)


def prepare_entangled(alpha, beta):
    """Construct a circuit that prepares the (not necessarily maximally) entangled state in terms of alpha and beta
    Do not forget to normalize.

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>
    """

    # QHACK #
     
    norm = np.sqrt(alpha**2+beta**2)
    theta = np.arctan(beta/alpha)
    
    #normalize alpha & beta
    alpha = alpha/norm
    beta = beta/norm
    
    qml.RY(2.0*theta,wires=0)
    qml.CNOT(wires=[0,1])
    # QHACK #

@qml.qnode(dev)
def chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, x, y, alpha, beta):
    """Construct a circuit that implements Alice's and Bob's measurements in the rotated bases

    Args:
        - theta_A0 (float): angle that Alice chooses when she receives x=0
        - theta_A1 (float): angle that Alice chooses when she receives x=1
        - theta_B0 (float): angle that Bob chooses when he receives x=0
        - theta_B1 (float): angle that Bob chooses when he receives x=1
        - x (int): bit received by Alice
        - y (int): bit received by Bob
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (np.tensor): Probabilities of each basis state
    """

    prepare_entangled(alpha, beta)

    # QHACK #

    #Set measurement angles based on values of the random bits x & y.
    if x==0:
        qml.RY(2.0*theta_A0,wires=0)        

    elif x==1:
        qml.RY(2.0*theta_A1,wires=0)

    if y==0:
        qml.RY(2.0*theta_B0,wires=1)        

    elif y==1:
        qml.RY(2.0*theta_B1,wires=1)

    # QHACK #

    return qml.probs(wires=[0, 1])
    

def winning_prob(params, alpha, beta):
    """Define a function that returns the probability of Alice and Bob winning the game.

    Args:
        - params (list(float)): List containing [theta_A0,theta_A1,theta_B0,theta_B1]
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning the game
    """

    pr_win = 0.0
    
    #Loop through all possible combinations of the random bits x and y.
    for x in range(2):
        for y in range(2):
            output = chsh_circuit(params[0], params[1], params[2], params[3], x, y, alpha, beta)        
            
            if (x*y==0):    
                #If x*y = 0, Alice & Bob must output 00 or 11 to win as, for addition modulo 2, 0 + 0 = 0 and 1 + 1 = 0.
                #So, for the measurement outcomes 00 and 11, x*y = a + b and hence Alice and Bob win. 
                pr_win += 0.25*(output[0] + output[3])
        
            elif (x*y==1):
                #If x*y = 1, Alice & Bob must output 01 or 10 to win as, for addition modulo 2, 0 + 1 = 1 and 1 + 0 = 1.
                #So, for the measurement outcomes 01 and 10, x*y = a + b and hence Alice and Bob win. 
                pr_win += 0.25*(output[1] + output[2])
    
    return pr_win
    # QHACK #
    

def optimize(alpha, beta):
    """Define a function that optimizes theta_A0, theta_A1, theta_B0, theta_B1 to maximize the probability of winning the game

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning
    """

    def cost(params):
        """Define a cost function that only depends on params, given alpha and beta fixed"""

    # QHACK #
        #Define the cost as the square loss between 1 (always winning) and the actual probability of winning.
        return (1 - winning_prob(params, alpha, beta))**2


    
    #Initialize parameters, choose an optimization method and number of steps
    #parameters are the four measurement angles: theta_A0, theta_A1, theta_B0, theta_B1
    
    #initial parameter values are NOT all zero as that corresponds to a local minimum and so causes the optimization to get stuck & fail.
    init_params = [0.5,0.5,0.0,1.0]
    opt = qml.GradientDescentOptimizer(stepsize=0.4)
    steps = 500

    # QHACK #
    params = np.zeros(4, requires_grad=True)

    #initialize params array
    params[:] = init_params[:]

    for i in range(steps):
        # update the circuit parameters 
        # QHACK #
        
        params = opt.step(cost,params) 
        
        # QHACK #

    return winning_prob(params, alpha, beta)


if __name__ == '__main__':
    inputs = sys.stdin.read().split(",")
    output = optimize(float(inputs[0]), float(inputs[1]))
    print(f"{output}")