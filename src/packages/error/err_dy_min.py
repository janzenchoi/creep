"""
 Title: The err_dy_min objective function
 Description: The objective function for calculating the differences between the minimute creep rates
 Author: Janzen Choi

"""

# Libraries
import numpy as np
import packages.error.objective as objective

# The ErrDyMin class
class ErrDyMin():

    # Constructor
    def __init__(self, exp_x_data, exp_y_data):
        self.name = "err_dy_min"
        self.exp_dy_min = [min(objective.get_fd(exp_x_data[i], exp_y_data[i])) for i in range(len(exp_x_data))]
    
    # Computing the error
    def get_error(self, prd_x_data, prd_y_data):
        prd_dy_min = [min(objective.get_fd(prd_x_data[i], prd_y_data[i])) for i in range(len(prd_x_data))]
        err_dy_min = [abs(prd_dy_min[i] - self.exp_dy_min[i]) / self.exp_dy_min[i] for i in range(len(self.exp_dy_min))]
        return np.average(err_dy_min)