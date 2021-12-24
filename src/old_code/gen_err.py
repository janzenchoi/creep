"""
 Title: Generator
 Description: For generating parameters and errors
 Author: Janzen Choi

"""

# Libraries
import time
import random
import packages.io.excel as excel
import packages.model.visco_plastic as visco_plastic
import packages.objective as objective

# Constants
DATA_PATH       = './'
DATA_FILE       = 'alloy_617'
RESULTS_PATH    = './results/'
NUM_PARAMS      = 50000
ERRORS          = ['err_area','err_x_end','err_y_end','err_mrate']

# The main function
def main():

    # Initialisation
    start_time = time.time()
    print('Program begun at ' + time.strftime('%H:%M:%S', time.localtime()) + '!')

    # Gets the experimental data at all stress values
    xl = excel.Excel(path = DATA_PATH, file = DATA_FILE)
    test_names = xl.read_included('test')
    exp_x_data = [xl.read_column(column = test_name + '_time', sheet = 'data') for test_name in test_names]
    exp_y_data = [xl.read_column(column = test_name + '_strain', sheet = 'data') for test_name in test_names]
    exp_stresses = xl.read_included('stress')
    print('The experimental data for ' + str(len(test_names)) + ' test(s) has been read!')

    # Initialise everything
    model = visco_plastic.ViscoPlastic(exp_stresses)
    obj = objective.Objective(model, exp_x_data, exp_y_data)
    bounds = [[model.l_bnds[i],  model.u_bnds[i]] for i in range(0,len(model.l_bnds))]
    print('The model has been initialised!')

    # Get the parameters
    params_list = get_params_list(bounds, NUM_PARAMS)
    print(str(NUM_PARAMS) + ' parameter(s) have been obtained!')

    # Evalute errors for each parameter
    print('\n===============================================================\n')
    errors_list = [[] for i in range(0,len(exp_stresses))]
    for i in range(0,len(params_list)):
        errors = get_errors(params_list[i], model, obj)
        for j in range(0,len(exp_stresses)):
            errors_list[j].append(errors[j])
        if ((i+1) % round(NUM_PARAMS/100)) == 0:
            print(' Evaluated parameters (' + str(round(((i+1) / round(NUM_PARAMS/100)))) + '%)!')
    print('\n===============================================================\n')
    print('Parameters have been evaluated!')

    # Write the results in a file
    data_names = model.params + ERRORS
    for i in range(0,len(exp_stresses)):
        data = [list(params_list[j]) + errors_list[i][j] for j in range(0,len(params_list))]
        xl = excel.Excel(path = RESULTS_PATH, file = 'params_' + str(exp_stresses[i]), sheet = 'params')
        xl.append_data(data, data_names)
    print('Results have been written!')

    # End message
    print('Program finished at ' + time.strftime('%H:%M:%S', time.localtime()) + ' in ' + str(round(time.time()-start_time)) + ' seconds!')

# Generates a list of randomised parameters in given bounds
def get_params_list(bounds, num_params):
    params_list = []
    for i in range(0,num_params):
        params_list.append([random.uniform(bounds[j][0], bounds[j][1]) for j in range(0,len(bounds))])
    return params_list

# Gets a list of errors given a set of parameters
def get_errors(params, model, obj):

    # Gets the predicted curves
    prd_x_data, prd_y_data = model.get_prd_curves(*params)

    # If predictions faield
    if prd_x_data == [] or prd_y_data == []:
        return [[objective.BIG_VALUE] * len(ERRORS)] * len(model.stresses)

    # Evaluate errors
    err_area  = obj.get_err_area(prd_x_data, prd_y_data)
    err_x_end = obj.get_err_x_end(prd_x_data, prd_y_data)
    err_y_end = obj.get_err_y_end(prd_x_data, prd_y_data)
    err_mrate = obj.get_err_mrate(prd_x_data, prd_y_data)
    
    # Record errors and return
    errors = [[err_area[j], err_x_end[j], err_y_end[j], err_mrate[j]] for j in range(0,len(model.stresses))]
    return errors

# Calls the main function
if __name__ == '__main__':
    main()