"""
 Title: Main file
 Description: Main file for creep prediction
 Author: Janzen Choi

"""

# Libraries
import time
import packages.io.excel as excel
import packages.io.recorder as recorder
import packages.model.visco_plastic as visco_plastic
import packages.error.objective as objective
import packages.genetic_algorithm as genetic_algorithm

# Constants
DATA_PATH       = './'
DATA_FILE       = 'alloy_617'
RECORD_PATH     = './results/'
RECORD_FOLDER   = 'optimisation'
TEST_NAMES      = ['G44','G25'] # ['G32', 'G33', 'G44', 'G25']
ERR_NAMES       = ['err_dy_min', 'err_x_area', 'err_x_fail'] # ['err_dy_min', 'err_x_area', 'err_y_area', 'err_x_fail', 'err_y_fail']

# Initialisation
start_time = time.time()
print('Program began on ' + time.strftime('%A, %D, %H:%M:%S', time.localtime()) + '!')

# Gets the experimental data
xl = excel.Excel(path = DATA_PATH, file = DATA_FILE)
exp_x_data = [xl.read_column(column = test_name + '_time', sheet = 'data') for test_name in TEST_NAMES]
exp_y_data = [xl.read_column(column = test_name + '_strain', sheet = 'data') for test_name in TEST_NAMES]
exp_stresses = xl.read_included('stress', TEST_NAMES)
print('The experimental data for ' + str(len(TEST_NAMES)) + ' test(s) has been read!')

# Prepares the optimisation
model = visco_plastic.ViscoPlastic(exp_stresses)
obj = objective.Objective(ERR_NAMES, exp_x_data, exp_y_data)
moga = genetic_algorithm.MOGA(model, obj)
rec = recorder.Recorder(model, obj, moga, path = RECORD_PATH, folder = RECORD_FOLDER)
print('The optimisation has been prepared')

# Conducts the optimisation
moga.set_recorder(rec)
moga.optimise()
print('The optimisation has concluded!')

# End message
print('Program finished on ' + time.strftime('%A, %D, %H:%M:%S', time.localtime()) + ' in ' + str(round(time.time()-start_time)) + ' seconds!')