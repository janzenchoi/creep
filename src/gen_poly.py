"""
 Title: Generator
 Description: For generating parameters and their curves
 Author: Janzen Choi

"""

# Libraries
import time
import math
import random
import numpy as np
import packages.io.excel as excel
import packages.model.visco_plastic as visco_plastic

# General Constants
POLY_DEG        = 15
DATA_DENSITY    = 50
NUM_SAMPLES     = 10000
STRESSES        = [80]

# Model Constants
PARAMS       = visco_plastic.PARAMS
L_BNDS       = visco_plastic.L_BNDS
U_BNDS       = visco_plastic.U_BNDS

# Naming Constants
DATA_PATH       = './'
DATA_FILE       = 'alloy_617'
PARAMS_PATH     = './'
PARAMS_FILE     = 'good_params_80'
PARAMS_SHEET    = 'params'
RESULTS_PATH    = './results/'
RESULTS_FILE    = 'generated_'
RESULTS_SHEET   = 'generated'

# The main function
def main():

    # Initialisation
    start_time = time.time()
    print('Program begun at ' + time.strftime('%H:%M:%S', time.localtime()) + '!')

    # Gets the list of parameters
    bounds = [[L_BNDS[i], U_BNDS[i]] for i in range(0, len(L_BNDS))]
    # params_list = get_random_params(bounds, NUM_SAMPLES)
    params_list = read_params(PARAMS_PATH, PARAMS_FILE, PARAMS_SHEET)
    print('Obtained ' + str(NUM_SAMPLES) + ' sets of parameters!')

    # Prepares the writer
    output_columns = PARAMS + ['x_end', 'y_end'] + ['c_' + str(term) for term in range(0, POLY_DEG+1)]
    xl = excel.Excel(path = RESULTS_PATH, file = '', sheet = RESULTS_SHEET)
    print('Prepared for recording values!')

    # Gets the outputs and writes it for each stress
    for stress in STRESSES:
        output_list = get_outputs(params_list, stress)
        xl.append_data(data = output_list, columns = output_columns, file = RESULTS_FILE + str(stress))
        print('Finished recording values at ' + str(stress) + ' MPa!')

    # End message
    print('Program finished at ' + time.strftime('%H:%M:%S', time.localtime()) + ' in ' + str(round(time.time()-start_time)) + ' seconds!')

# Reads a list of parameters
def read_params(path, file, sheet):
    xl = excel.Excel(path = path, file = file, sheet = sheet)
    params_list = [xl.read_column(column=param) for param in PARAMS] # reads all the parameters
    params_list = [[param[i] for param in params_list] for i in range(0,len(params_list[0]))] # transposes
    return params_list

# Generates a list of randomised parameters in given bounds
def get_random_params(bounds, num_samples):
    params_list = []
    for i in range(0, num_samples):
        params_list.append([random.uniform(bounds[j][0], bounds[j][1]) for j in range(0,len(bounds))])
    return params_list

# Returns a list of indexes corresponding to thinned data
def get_thin_indexes(src_data_size, dst_data_size):
    step_size = src_data_size/dst_data_size
    thin_indexes = [math.floor(step_size*i) for i in range(1,dst_data_size-1)]
    thin_indexes = [0] + thin_indexes + [src_data_size-1]
    return thin_indexes

# Gets the output of the driver based on a set of parameters
def get_outputs(params_list, stress):
    
    # Gets the V-P model
    model = visco_plastic.ViscoPlastic([stress])

    # For each set of parameters, get the outputs
    output_list = []
    for i in range(0, len(params_list)):

        # Gets the curves from the V-P model's driver
        x_data, y_data = model.get_prd_curves(*params_list[i])

        # If driver failed, return an empty polynomial
        if x_data == [] or y_data == []:
            output_list.append(params_list[i] + [0] * (2 + POLY_DEG + 1))
            continue

        # Sparsen the data
        thin_indexes = get_thin_indexes(len(x_data[0]), DATA_DENSITY)
        x_list = [x_data[0][j] for j in thin_indexes]
        y_list = [y_data[0][j] for j in thin_indexes]

        # Gets the end point and fitted polynomial
        x_end, y_end = max(x_list), max(y_list)
        polynomial = list(np.polyfit(x_list, y_list, POLY_DEG))
        output_list.append(params_list[i] + [x_end, y_end] + polynomial)

    # Return the output list
    return output_list

# Calls the main function
if __name__ == '__main__':
    main()