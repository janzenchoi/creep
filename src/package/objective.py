"""
 Title: The Objective Function class
 Description: The objective functions for the MOGA to minimise
 Author: Janzen Choi

"""

# Libraries
import math
import numpy as np
from pymoo.model.problem import Problem

# Constants
POLY_DEG     = 15
DATA_DENSITY = 50
BIG_VALUE    = 100
ERRORS       = ['err_area','err_x_end','err_y_end']

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
        dy = -BIG_VALUE
        if (x_list[i] != x_list[i-1] and y_list[i] > y_list[i-1]):
            dy = (y_list[i]-y_list[i-1])/(x_list[i]-x_list[i-1])
        dy_list.append(dy)
    return dy_list

# The Objective class
class Objective(Problem):

    # Constructor
    def __init__(self, model, exp_x_data, exp_y_data):

        # Initialise errors
        self.errors = ERRORS

        # Initialise recorder
        self.rec = None

        # Initialise experimental data
        self.exp_x_data, self.exp_y_data = exp_x_data, exp_y_data
        self.exp_poly, self.exp_x_end, self.exp_y_end, self.exp_mrate = [], [], [], []
        for i in range(0,len(exp_x_data)):
            self.exp_poly.append(list(np.polyfit(exp_x_data[i], exp_y_data[i], POLY_DEG)))
            self.exp_x_end.append(max(exp_x_data[i]))
            self.exp_y_end.append(exp_y_data[i][exp_x_data[i].index(max(exp_x_data[i]))])
            self.exp_mrate.append(min(np.polyval(np.polyder(self.exp_poly[i]), exp_x_data[i])))
        self.avg_y_list = [np.average(y) for y in self.exp_y_data]

        # Initialise optimisation problem
        self.model = model
        super().__init__(
            n_var    = len(model.params),
            n_obj    = len(self.errors),
            n_constr = 0,
            xl       = np.array(model.l_bnds),
            xu       = np.array(model.u_bnds),
            elementwise_evaluation = True)

    # Get the area between the experimental and predicted curves
    def get_err_area(self, prd_x_data, prd_y_data):
        err_area = []
        for i in range(0, len(prd_x_data)):
            
            # Thins the predicted and experimental data
            thin_indexes = get_thin_indexes(len(prd_x_data[i]), DATA_DENSITY)
            prd_x_list = [prd_x_data[i][j] for j in thin_indexes]
            prd_y_list = [prd_y_data[i][j] for j in thin_indexes]
            exp_y_list = list(np.polyval(self.exp_poly[i], prd_x_list))

            # Consider the area only between the two curves
            area, valid_points = 0, 0
            for j in range(0, DATA_DENSITY):
                if prd_x_list[j] <= self.exp_x_end[i]:
                    area += abs(prd_y_list[j] - exp_y_list[j])
                    valid_points += 1
            err_area.append(area / valid_points / self.avg_y_list[i])

        # Return list of normalised area errors
        return err_area

    # Gets the horizontal distance between the endpoints of the experimental and predicted curves
    def get_err_x_end(self, prd_x_data, prd_y_data):
        prd_x_end = [max(prd_x_data[i]) for i in range(0, len(prd_x_data))]
        err_x_end = [abs(prd_x_end[i] - self.exp_x_end[i]) / self.exp_x_end[i] for i in range(0, len(prd_x_data))]
        return err_x_end

    # Gets the vertical distance between the endpoints of the experimental and predicted curves
    def get_err_y_end(self, prd_x_data, prd_y_data):
        prd_y_end = [prd_y_data[i][prd_x_data[i].index(max(prd_x_data[i]))] for i in range(0,len(prd_x_data))]
        err_y_end = [abs(prd_y_end[i] - self.exp_y_end[i]) / self.exp_y_end[i] for i in range(0, len(prd_y_data))]
        return err_y_end

    # Gets the difference between the minimum creep rates of the experimental and predicted curves
    def get_err_mrate(self, prd_x_data, prd_y_data):
        prd_mrate = [min(get_fd(prd_x_data[i], prd_y_data[i])) for i in range(0,len(prd_x_data))]
        err_mrate = [abs(prd_mrate[i] - self.exp_mrate[i]) / self.exp_mrate[i] for i in range(0,len(prd_x_data))]
        return err_mrate

    # Sets a recorder that records the results during the optimisations
    def set_recorder(self, rec):
        self.rec = rec

    # Returns a list of errors given a set of parameters
    def get_errors(self, params):

        # Get the predicted curves
        prd_x_data, prd_y_data = self.model.get_prd_curves(*params)

        # Get the errors
        if prd_x_data == [] or prd_y_data == []:
            err_list = [BIG_VALUE] * len(self.errors)
        else:
            err_list = []
            for err in self.errors:
                if (err == 'err_area'):
                    err_list.append(np.average(self.get_err_area(prd_x_data, prd_y_data)))
                elif (err == 'err_x_end'):
                    err_list.append(np.average(self.get_err_x_end(prd_x_data, prd_y_data)))
                elif (err == 'err_y_end'):
                    err_list.append(np.average(self.get_err_y_end(prd_x_data, prd_y_data)))
                elif (err == 'err_mrate'):  
                    err_list.append(np.average(self.get_err_mrate(prd_x_data, prd_y_data)))

        # If a recorder was set, then record the results
        if (self.rec != None):
            self.rec.update_record(params, err_list)

        # Return the error list
        return err_list

    # Minimises expression 'F' such that the expression 'G <= 0' is satisfied
    def _evaluate(self, params, out, *args, **kwargs):
        out['F'] = self.get_errors(params)