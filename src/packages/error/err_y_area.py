"""
 Title: The err_y_area objective function
 Description: The objective function for calculating the vertical areas between two curves
 Author: Janzen Choi

"""

# Libraries
import packages.error.objective as objective
import numpy as np

# Constants
POLY_DEG    = 15 # has to be odd
NUM_POINTS  = 100

# The ErrYArea class
class ErrYArea():

    # Constructor
    def __init__(self, exp_x_data, exp_y_data):
        self.name = "err_y_area"
        self.exp_polynomials = [list(np.polyfit(exp_x_data[i], exp_y_data[i], POLY_DEG)) for i in range(len(exp_x_data))]
        self.exp_x_end = [max(exp_x_list) for exp_x_list in exp_x_data]
        self.avg_y_list = [np.average(exp_y_list) for exp_y_list in exp_y_data]

    # Computing the error
    def get_error(self, prd_x_data, prd_y_data):
        err_y_area = []
        for i in range(len(prd_x_data)):
            thin_indexes = objective.get_thin_indexes(len(prd_x_data[i]), NUM_POINTS)
            prd_x_list = [prd_x_data[i][j] for j in thin_indexes]
            prd_y_list = [prd_y_data[i][j] for j in thin_indexes]
            exp_y_list = list(np.polyval(self.exp_polynomials[i], prd_x_list))
            area = [abs(prd_y_list[j] - exp_y_list[j]) for j in range(NUM_POINTS) if prd_x_list[j] <= self.exp_x_end[i]]
            err_y_area.append(np.average(area) / self.avg_y_list[i])
        return np.average(err_y_area)