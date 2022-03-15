"""
 Title: The err_x_end objective function
 Description: The objective function for calculating the horizontal distance in which two curves end
 Author: Janzen Choi

"""

# Libraries
import numpy as np

# The ErrXEnd class
class ErrXEnd():

    # Constructor
    def __init__(self, exp_x_data, _):
        self.name = "err_x_end"
        self.exp_x_end = [max(exp_x_list) for exp_x_list in exp_x_data]
    
    # Computing the error
    def get_error(self, prd_x_data, _):
        prd_x_end = [max(prd_x_data[i]) for i in range(0, len(prd_x_data))]
        err_x_end = [abs(prd_x_end[i] - self.exp_x_end[i]) / self.exp_x_end[i] for i in range(len(self.exp_x_end))]
        return np.average(err_x_end)