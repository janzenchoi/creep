"""
 Title: Sampler
 Description: For sampling inputs/outputs for machine learning
 Author: Janzen Choi

"""

# Libraries
import random
import packages.polyfier as polyfier
import packages.io.excel as excel
import packages.model.visco_plastic as visco_plastic

# Constants
POLY_DEG    = polyfier.DEFAULT_POLY_DEG
PARAMS_LIST = visco_plastic.PARAMS
COEFFS_LIST = ['c_' + str(term) for term in range(0, POLY_DEG + 1)]
INPUT_PATH  = './results/param_sets/'
INPUT_FILE  = 'wide_80_15'
INPUT_SHEET = 'params'

# For sampling parameters
class Sampler:

    # Constructor
    def __init__(self):
        xl = excel.Excel(path = INPUT_PATH, file = INPUT_FILE, sheet = INPUT_SHEET)
        print(PARAMS_LIST)
        self.params_list = xl.read_columns(columns = PARAMS_LIST)
        self.x_end_list  = xl.read_column(column = 'x_end')
        self.coeffs_list = xl.read_columns(columns = COEFFS_LIST)
        self.index_list  = [i for i in range(0, len(self.params_list))]
        random.shuffle(self.index_list)

    # Reads random parameters and errors
    def sample(self, num_samples):
        
        # Gets a list of random indexes
        index_list = [self.index_list.pop(0) for i in range(0, num_samples)]
        
        # Gets the inputs (params)
        input_list = [self.params_list[i] for i in index_list]
        
        # Gets the outputs (y values)
        output_list = []
        pf = polyfier.Polyfier()
        for i in index_list:
            _, y_list = pf.polynomial_to_curve(self.x_end_list[i], self.coeffs_list[i])
            output_list.append(y_list)

        # Return input and output
        return input_list, output_list