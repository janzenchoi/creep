"""
 Title: Polynomial conversion functions
 Description: Functions for converting a curve into a polynomial and vice versa
 Author: Janzen Choi

"""

# Libraries
import numpy as np

# Constants
POLY_DEG        = 15
X_STEP_SIZE     = 5
MAX_LIST_SIZE   = 500
INVALID_NUMBER  = 0

# Get a list of x values based on the constants
def get_x_list(y_list):
    x_list = [X_STEP_SIZE * i for i in range(0, len(y_list))]
    return x_list

# Removes invalid numbers from a list
def process(unprocessed_list):

    # Initialise
    unprocessed_list = [abs(u) for u in unprocessed_list]
    processed_list = []
    previous = -1

    # Process the lsit
    for current in unprocessed_list:
        if current >= previous:
            processed_list.append(current)
            previous = current
        else:
            break

    # Return the processed list
    return processed_list

# Converts a list of values into a polynomial
def curve_to_polynomial(y_list):

    # Get x and y lists without invalid numbers
    y_list = process(y_list)
    x_list = get_x_list(y_list)

    # Get the failure point and polynomial
    x_end = max(x_list)
    polynomial = list(np.polyfit(x_list, y_list, POLY_DEG))
    
    # Return the failure point and polynomial
    return x_end, polynomial

# Converts a polynomial into x and y lists
def polynomial_to_curve(x_end, polynomial):
    
    # Get x and y lists
    list_size = round(x_end / X_STEP_SIZE)
    x_list = [X_STEP_SIZE * i for i in range(0, list_size)]
    y_list = list(np.polyval(polynomial, x_list))
    
    # Pad the lists with invalid numbers
    for i in range(0, MAX_LIST_SIZE - len(x_list)):
        x_list.append(INVALID_NUMBER)
        y_list.append(INVALID_NUMBER)

    # Return the x and y lists
    return x_list, y_list
