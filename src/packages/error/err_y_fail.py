"""
 Title: The err_yfail objective function
 Description: The objective function for calculating the vertical distance in which two curves end
 Author: Janzen Choi

"""

# Libraries
import numpy as np

# The ErrYFail class
class ErrYFail():

    # Constructor
    def __init__(self, _, exp_y_data):
        self.name = "err_y_fail"
        self.exp_y_fail = [max(exp_y_list) for exp_y_list in exp_y_data]
    
    # Computing the error
    def get_error(self, _, prd_y_data):
        prd_y_fail = [max(prd_y_data[i]) for i in range(0, len(prd_y_data))]
        err_y_fail = [abs(prd_y_fail[i] - self.exp_y_fail[i]) / self.exp_y_fail[i] for i in range(len(self.exp_y_fail))]
        return np.average(err_y_fail)