"""
 Title: The err_y_end objective function
 Description: The objective function for calculating the vertical distance in which two curves end
 Author: Janzen Choi

"""

# Libraries
import numpy as np

# The ErrYEnd class
class ErrYEnd():

    # Constructor
    def __init__(self, _, exp_y_data):
        self.name = "err_y_end"
        self.exp_y_end = [max(exp_y_list) for exp_y_list in exp_y_data]
    
    # Computing the error
    def get_error(self, _, prd_y_data):
        prd_y_end = [max(prd_y_data[i]) for i in range(0, len(prd_y_data))]
        err_y_end = [abs(prd_y_end[i] - self.exp_y_end[i]) / self.exp_y_end[i] for i in range(len(self.exp_y_end))]
        return np.average(err_y_end)