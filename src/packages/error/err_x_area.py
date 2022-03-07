"""
 Title: The err_x_area objective function
 Description: The objective function for calculating the vertical areas between two curves
 Author: Janzen Choi

"""

# Libraries
import packages.error.objective as objective
import numpy as np

# Constants
POLY_DEG    = 16 # has to be even
NUM_POINTS  = 50

# The ErrXArea class
class ErrXArea():

    # Constructor
    def __init__(self, exp_x_data, exp_y_data):
        self.name = "err_x_area"
        self.exp_polynomials = [list(np.polyfit(exp_y_data[i], exp_x_data[i], POLY_DEG)) for i in range(len(exp_x_data))] # inverted
        self.exp_y_fail = [max(exp_y_list) for exp_y_list in exp_y_data]
        self.avg_x_list = [np.average(exp_x_list) for exp_x_list in exp_x_data]

    # Computing the error
    def get_error(self, prd_x_data, prd_y_data):
        err_x_area = []
        for i in range(len(prd_x_data)):
            
            # Get predicted and experimental data
            thin_indexes = objective.get_thin_indexes(len(prd_x_data), NUM_POINTS)
            prd_x_list = [prd_x_data[i][j] for j in thin_indexes]
            prd_y_list = [prd_y_data[i][j] for j in thin_indexes]
            exp_x_list = list(np.polyval(self.exp_polynomials[i], prd_y_list))

            # Computer error
            area, valid_points = 0, 0
            for j in range(0, NUM_POINTS):
                if prd_y_list[j] <= self.exp_y_fail[i]:
                    area += abs(prd_x_list[j] - exp_x_list[j])
                    valid_points += 1
            err_x_area.append(area / valid_points / self.avg_x_list[i])
            
        return np.average(err_x_area)