"""
 Title: The Objective Function class
 Description: The objective functions for the MOGA to minimise
 Author: Janzen Choi

"""

# Libraries
import math
import numpy
from pymoo.model.problem import Problem

# Constants
POLY_DEG = 15
DATA_DENSITY = 50
BIG_VALUE = 100

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
    def __init__(self, visco, exp_x_data, exp_y_data):

        # Initialise errors
        self.errors = ['err_area','err_x_end','err_y_end']

        # Initialise experimental data
        self.exp_x_data = exp_x_data
        self.exp_y_data = exp_y_data
        self.exp_poly, self.exp_x_end, self.exp_y_end, self.exp_mrate = [], [], [], []
        for i in range(0,len(exp_x_data)):
            self.exp_poly.append(list(numpy.polyfit(exp_x_data[i], exp_y_data[i], POLY_DEG)))
            self.exp_x_end.append(max(exp_x_data[i]))
            self.exp_y_end.append(exp_y_data[i][exp_x_data[i].index(max(exp_x_data[i]))])
            self.exp_mrate.append(min(numpy.polyval(numpy.polyder(self.exp_poly[i]), exp_x_data[i])))

        # Get the mean of the experimental data values
        self.avg_y = numpy.average([numpy.average(y) for y in self.exp_y_data])
        self.avg_x_end = numpy.average(self.exp_x_end)
        self.avg_y_end = numpy.average(self.exp_y_end)
        self.avg_mrate = numpy.average(self.exp_mrate)

        # Initialise optimisation problem
        self.visco = visco
        super().__init__(
            n_var    = len(visco.params),
            n_obj    = len(self.errors),
            n_constr = 0,
            xl       = numpy.array(visco.l_bnds),
            xu       = numpy.array(visco.u_bnds),
            elementwise_evaluation = True)

    # Get the area between the experimental and predicted curves
    def get_err_area(self, prd_x_data, prd_y_data):
        err_area, valid_points = 0, 0
        for i in range(0, len(prd_x_data)):
            
            # Thins the predicted and experimental data
            thin_indexes = get_thin_indexes(len(prd_x_data[i]), DATA_DENSITY)
            prd_x_list = [prd_x_data[i][j] for j in thin_indexes]
            prd_y_list = [prd_y_data[i][j] for j in thin_indexes]
            exp_y_list = list(numpy.polyval(self.exp_poly[i], prd_x_list))

            # Consider the area only between the two curves
            for j in range(0, DATA_DENSITY):
                if prd_x_list[j] <= self.exp_x_end[i]:
                    err_area += abs(prd_y_list[j] - exp_y_list[j])
                    valid_points += 1

        # Return normalised area
        return err_area / valid_points / self.avg_y

    # Gets the horizontal distance between the endpoints of the experimental and predicted curves
    def get_err_x_end(self, prd_x_data, prd_y_data):
        prd_x_end = [max(prd_x_data[i]) for i in range(0, len(prd_x_data))]
        err_x_end = sum([abs(prd_x_end[i] - self.exp_x_end[i]) for i in range(0, len(prd_x_data))])
        return err_x_end / len(prd_x_end) / self.avg_x_end

    # Gets the vertical distance between the endpoints of the experimental and predicted curves
    def get_err_y_end(self, prd_x_data, prd_y_data):
        prd_y_end = [prd_y_data[i][prd_x_data[i].index(max(prd_x_data[i]))] for i in range(0,len(prd_x_data))]
        err_y_end = sum([abs(prd_y_end[i] - self.exp_y_end[i]) for i in range(0, len(prd_y_data))])
        return err_y_end / len(prd_x_data) / self.avg_y_end

    # Gets the difference between the minimum creep rates of the experimental and predicted curves
    def get_err_mrate(self, prd_x_data, prd_y_data):
        prd_mrate = [min(get_fd(prd_x_data[i], prd_y_data[i])) for i in range(0,len(prd_x_data))]
        err_mrate = sum([abs(prd_mrate[i] - self.exp_mrate[i]) for i in range(0,len(prd_x_data))])
        return err_mrate / len(prd_x_data) / self.avg_mrate

    # Minimises expression 'F' such that the expression 'G <= 0' is satisfied
    def _evaluate(self, params, out, *args, **kwargs):

        # Get the predicted curves
        prd_x_data, prd_y_data = self.visco.get_prd_curves(*params)
        if prd_x_data == [] or prd_y_data == []:
            out['F'] = [BIG_VALUE] * len(self.errors)
            return

        # Get the error values
        err_list = []
        for err in self.errors:
            if (err == 'err_area'):
                err_list.append(self.get_err_area(prd_x_data, prd_y_data))
            elif (err == 'err_x_end'):
                err_list.append(self.get_err_x_end(prd_x_data, prd_y_data))
            elif (err == 'err_y_end'):
                err_list.append(self.get_err_y_end(prd_x_data, prd_y_data))
            elif (err == 'err_mrate'):  
                err_list.append(self.get_err_mrate(prd_x_data, prd_y_data))

        # Set objective functions
        out['F'] = err_list