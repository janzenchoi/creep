"""
 Title: Polynomial conversion functions
 Description: Functions for converting a curve into a polynomial and vice versa
 Author: Janzen Choi

"""

# Libraries
import numpy as np

# Constants
DEFAULT_POLY_DEG    = 15
DEFAULT_NUM_POINTS  = 100

# For converting polynomials into curves and vice cersa
class Polyfier:

    # Constructor
    def __init__(self, poly_deg = DEFAULT_POLY_DEG, num_points = DEFAULT_NUM_POINTS):
        self.poly_deg = poly_deg
        self.num_points = num_points

    # Gets a list of x values
    def get_x_list(self, x_end):
        x_list = np.linspace(0, x_end, num = self.num_points, endpoint = True)
        return x_list

    # Converts a list of values into a polynomial
    def curve_to_polynomial(self, x_list, y_list):
        x_end = max(x_list)
        polynomial = list(np.polyfit(x_list, y_list, self.poly_deg))
        return x_end, polynomial

    # Converts a polynomial into x and y lists
    def polynomial_to_curve(self, x_end, polynomial):
        x_list = self.get_x_list(x_end)
        y_list = list(np.polyval(polynomial, x_list))
        return x_list, y_list