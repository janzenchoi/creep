"""
 Title: Main file
 Description: Main file for creep prediction
 Author: Janzen Choi

"""

# Libraries
import time
import excel
import plot
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
print('The experimental data has been read!')

# Prepares the optimisation
visco = visco_plastic.ViscoPlastic(exp_stresses)
obj = objective.Objective(visco, exp_x_data, exp_y_data)
moga = genetic_algorithm.MOGA(obj)
params_list = moga.optimise()
print('The optimisation has concluded!')

# Gets the predicted parameters
params = params_list[0]
prd_x_data, prd_y_data = visco.get_prd_curves(*params)
print('The predicted curves have been obtained!')

# Plots the data
plot.prep_plot()
plot.exp_plot(exp_x_data, exp_y_data)
plot.prd_plot(prd_x_data, prd_y_data)
plot.save_plot()
print('The data has been plotted!')

# Writes the data
excel.write_columns(params_list, visco.params)

# End message
print('Program has finished in '+str(round(time.time()-start_time))+' seconds!')