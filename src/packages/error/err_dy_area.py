"""
 Title: The err_dy_area objective function
 Description: The objective function for calculating the vertical areas between the derivatives of two curves
 Author: Janzen Choi

"""

# Libraries
import packages.error.objective as objective
import numpy as np

# Constants
POLY_DEG    = 15 # has to be odd
NUM_POINTS  = 50

# The ErrDyArea class
class ErrDyArea():

    # Constructor
    def __init__(self, exp_x_data, exp_y_data):
        self.name = "err_dy_area"
        self.exp_polyder = [list(np.polyder(np.polyfit(exp_x_data[i], exp_y_data[i], POLY_DEG))) for i in range(len(exp_x_data))]
        self.exp_x_fail = [max(exp_x_list) for exp_x_list in exp_x_data]
        self.avg_dy_list = [np.average(np.polyval(self.exp_polyder[i], exp_x_data[i])) for i in range(len(exp_x_data))]

    # Computing the error
    def get_error(self, prd_x_data, prd_y_data):
        err_dy_area = []
        for i in range(len(prd_x_data)):
            thin_indexes = objective.get_thin_indexes(len(prd_x_data[i]), NUM_POINTS)
            prd_x_list = [prd_x_data[i][j] for j in thin_indexes]
            prd_y_list = [prd_y_data[i][j] for j in thin_indexes]
            prd_dy_list = objective.get_fd(prd_x_list, prd_y_list)
            exp_dy_list = list(np.polyval(self.exp_polyder[i], prd_x_list))
            area = [abs(prd_dy_list[j] - exp_dy_list[j]) for j in range(NUM_POINTS-1) if prd_x_list[j] <= self.exp_x_fail[i]]
            err_dy_area.append(np.average(area) / self.avg_dy_list[i])
        return np.average(err_dy_area)