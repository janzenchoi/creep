"""
 Title: Polynomial conversion functions
 Description: Functions for converting a curve into a polynomial and vice versa
 Author: Janzen Choi

"""

# Libraries
import numpy as np

# General constants
DEFAULT_POLY_DEG        = 15
DEFAULT_NUM_POINTS      = 100

# Constants for invalid values
DEFAULT_UPPER_BOUND     = 15000
DEFAULT_STEP_SIZE       = 50
DEFAULT_INVALID_VALUE   = 0

# For converting polynomials into curves and vice cersa
class Polyfier:

    # Constructor
    def __init__(self, poly_deg = DEFAULT_POLY_DEG, num_points = DEFAULT_NUM_POINTS):
        self.poly_deg = poly_deg
        self.num_points = num_points

    # Gets a list of stretched x values
    def get_stretched_x_list(self, x_end):
        x_list = np.linspace(0, x_end, num = self.num_points, endpoint = True)
        return x_list

    # Converts a list of values into a polynomial
    def curve_to_polynomial(self, x_list, y_list):
        x_end = max(x_list)
        polynomial = list(np.polyfit(x_list, y_list, self.poly_deg))
        return x_end, polynomial

    # Converts a polynomial into stretched x and y lists
    def polynomial_to_stretched_curve(self, x_end, polynomial):
        x_list = self.get_stretched_x_list(x_end)
        y_list = list(np.polyval(polynomial, x_list))
        return x_list, y_list

    # Gets a list of x values
    def get_x_list(self, num_points):
        x_list = [DEFAULT_STEP_SIZE * i for i in range(0, num_points)]
        return x_list

    # Converts a polynomial into x and y lists with invalid values
    def polynomial_to_curve(self, x_end, polynomial):
        
        # Gets the valid points
        max_points = round(DEFAULT_UPPER_BOUND / DEFAULT_STEP_SIZE)
        num_valid_points = min(round(x_end / DEFAULT_STEP_SIZE), max_points)
        x_list = self.get_x_list(num_valid_points)
        y_list = list(np.polyval(polynomial, x_list))
        
        # Gets the invalid points
        num_invalid_points = round(DEFAULT_UPPER_BOUND / DEFAULT_STEP_SIZE) - num_valid_points
        x_list = self.get_x_list(num_valid_points + num_invalid_points)
        y_list += [DEFAULT_INVALID_VALUE] * num_invalid_points
        
        # Return lists
        return x_list, y_list
    
    # Converts a list of x and y lists of any size into ones with the set step size
    def curves_to_curves(self, x_data, y_data):
        new_x_data, new_y_data = [], []
        for i in range(0, len(x_data)):
            x_end, polynomial = self.curve_to_polynomial(x_data[i], y_data[i])
            x_list, y_list = self.polynomial_to_curve(x_end, polynomial)
            new_x_data.append(x_list)
            new_y_data.append(y_list)
        return new_x_data, new_y_data