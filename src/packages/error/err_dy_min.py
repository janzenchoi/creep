"""
 Title: The err_dy_min objective function
 Description: The objective function for calculating the differences between the minimute creep rates
 Author: Janzen Choi

"""

# Libraries
import numpy as np

# The ErrMRate class
class ErrMRate():

    # Constructor
    def __init__(self, exp_x_data, exp_y_data):
        self.name = "err_dy_min"
        self.err_dy_min = [min(get_fd(exp_x_data[i], exp_y_data[i])) for i in range(len(exp_x_data))]
    
    # Computing the error
    def get_error(self, prd_x_data, prd_y_data):
        prd_dy_min = [min(get_fd(prd_x_data[i], prd_y_data[i])) for i in range(len(prd_x_data))]
        err_dy_min = [abs(prd_dy_min[i] - self.err_dy_min[i]) / self.err_dy_min[i] for i in range(len(self.err_dy_min))]
        return np.average(err_dy_min)

# Returns the derivative via finite difference
def get_fd(x_list, y_list):
    dy_list = []
    for i in range(1,len(x_list)):
        dy = 100
        if (x_list[i] != x_list[i-1] and y_list[i] > y_list[i-1]):
            dy = (y_list[i]-y_list[i-1])/(x_list[i]-x_list[i-1])
        dy_list.append(dy)
    return dy_list