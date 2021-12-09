"""
 Title: Main file
 Description: Main file for creep prediction
 Author: Janzen Choi

"""

# Libraries
import time
import excel
import recorder
import visco_plastic
import objective
import genetic_algorithm

# Constants

# Initialisation
start_time = time.time()
print('Program has begun!')

# Gets the experimental data
test_names = excel.read_included('test')
exp_x_data = [excel.read_column(test_name + '_time', excel.STRAIN_SHEET) for test_name in test_names]
exp_y_data = [excel.read_column(test_name + '_strain', excel.STRAIN_SHEET) for test_name in test_names]
exp_stresses = excel.read_included('stress')
print('The experimental data for ' + str(len(test_names)) + ' tests has been read!')

# Prepares the optimisation
model = visco_plastic.ViscoPlastic(exp_stresses)
obj = objective.Objective(model, exp_x_data, exp_y_data)
moga = genetic_algorithm.MOGA(obj)
rec = recorder.Recorder(model, obj, moga)
print('The optimisation has been prepared')

# Conducts the optimisation
obj.set_recorder(rec)
moga.optimise()
print('The optimisation has concluded!')

# End message
print('Program has finished in '+str(round(time.time()-start_time))+' seconds!')