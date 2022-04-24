#! /usr/bin/python3

import sys
import numpy as np


def givens_rotations(a, b, c, d):
    """Calculates the angles needed for a Givens rotation to out put the state with amplitudes a,b,c and d

    Args:
        - a,b,c,d (float): real numbers which represent the amplitude of the relevant basis states (see problem statement). Assume they are normalized.

    Returns:
        - (list(float)): a list of real numbers ranging in the intervals provided in the challenge statement, which represent the angles in the Givens rotations,
        in order, that must be applied.
    """

    # QHACK #

    """
    |psi> = cos(theta_1/2) cos(theta_3/2) |110000> - sin(theta_1/2) cos(theta_2/2) |110000> + sin(theta_1/2) sin(theta_2/2) |110000> 
    - cos(theta_1/2) sin(theta_3/2) |100100>
    
    Equating coefficients, we get:
        a = cos(theta_1/2) cos(theta_3/2)
        b = -sin(theta_1/2) cos(theta_2/2)
        c = sin(theta_1/2) sin(theta_2/2)
        d = -cos(theta_1/2) sin(theta_3/2) 
        
    Solving the above four equations for theta_1, theta_2, and theta_3 gives:        
    """

    theta_2=2*np.arctan(-c/b)    
    theta_1= 2*np.arcsin(c/(np.sin(theta_2/2)))
    theta_3=2*np.arcsin(-d/(np.cos(theta_1/2)))

    thetas=[theta_1,theta_2,theta_3]

    return thetas

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    theta_1, theta_2, theta_3 = givens_rotations(
        float(inputs[0]), float(inputs[1]), float(inputs[2]), float(inputs[3])
    )
    print(*[theta_1, theta_2, theta_3], sep=",")
