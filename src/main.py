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
import packages.objective as objective
import packages.genetic_algorithm as genetic_algorithm

# Constants
DATA_PATH = './'
DATA_FILE = 'alloy_617'
RECORD_PATH = './results/'
RECORD_FOLDER = 'optimisation'

# Initialisation
start_time = time.time()
print('Program began on ' + time.strftime('%A, %D, %H:%M:%S', time.localtime()) + '!')

# Gets the experimental data
xl = excel.Excel(path = DATA_PATH, file = DATA_FILE)
test_names = xl.read_included('test')
exp_x_data = [xl.read_column(column = test_name + '_time', sheet = 'data') for test_name in test_names]
exp_y_data = [xl.read_column(column = test_name + '_strain', sheet = 'data') for test_name in test_names]
exp_stresses = xl.read_included('stress')
print('The experimental data for ' + str(len(test_names)) + ' test(s) has been read!')

# Prepares the optimisation
model = visco_plastic.ViscoPlastic(exp_stresses)
obj = objective.Objective(model, exp_x_data, exp_y_data)
moga = genetic_algorithm.MOGA(obj)
rec = recorder.Recorder(model, obj, moga, path = RECORD_PATH, folder = RECORD_FOLDER)
print('The optimisation has been prepared')

# Conducts the optimisation
obj.set_recorder(rec)
moga.optimise()
print('The optimisation has concluded!')

# End message
print('Program finished on ' + time.strftime('%A, %D, %H:%M:%S', time.localtime()) + ' in ' + str(round(time.time()-start_time)) + ' seconds!')