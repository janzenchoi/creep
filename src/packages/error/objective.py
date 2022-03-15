"""
 Title: The Objective class
 Description: A class for storing multiple errors
 Author: Janzen Choi

"""

# Libraries
import math
import packages.error.err_dy_min as err_dy_min
import packages.error.err_dy_area as err_dy_area
import packages.error.err_x_end as err_x_end
import packages.error.err_y_end as err_y_end
import packages.error.err_x_area as err_x_area
import packages.error.err_y_area as err_y_area

# Constants
BIG_VALUE = 100

# The Objective class
class Objective():

    # Constructor
    def __init__(self, err_names, exp_x_data, exp_y_data):
        self.exp_x_data = exp_x_data
        self.exp_y_data = exp_y_data
        self.err_collection = [err_dy_min.ErrDyMin(exp_x_data, exp_y_data),
                               err_dy_area.ErrDyArea(exp_x_data, exp_y_data),
                               err_x_end.ErrXEnd(exp_x_data, exp_y_data),
                               err_y_end.ErrYEnd(exp_x_data, exp_y_data),
                               err_x_area.ErrXArea(exp_x_data, exp_y_data),
                               err_y_area.ErrYArea(exp_x_data, exp_y_data)]
        self.err_collection = [err for err in self.err_collection if err.name in err_names]
    
    # Get objective names
    def get_error_names(self):
        return [err.name for err in self.err_collection]

    # Get all the errors
    def get_errors(self, prd_x_data, prd_y_data):
        if prd_x_data == [] or prd_y_data == []:
            return [BIG_VALUE] * len(self.err_collection)
        err_list = [err.get_error(prd_x_data, prd_y_data) for err in self.err_collection]
        return err_list

# Returns a list of indexes corresponding to thinned data
def get_thin_indexes(src_data_size, dst_data_size):
    step_size = src_data_size/dst_data_size
    thin_indexes = [math.floor(step_size*i) for i in range(1,dst_data_size-1)]
    thin_indexes = [0] + thin_indexes + [src_data_size-1]
    return thin_indexes

# Returns the derivative via finite difference
def get_fd(x_list, y_list):
    dy_list = []
    for i in range(1,len(x_list)):
        dy = (y_list[i]-y_list[i-1])/(x_list[i]-x_list[i-1]) if (x_list[i] > x_list[i-1] and y_list[i] > y_list[i-1]) else 100
        dy_list.append(dy)
    return dy_list