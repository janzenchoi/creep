"""
 Title: Main file for plotting
 Description: Main file for plotting prediction results
 Author: Janzen Choi

"""

# Libraries
import time
import packages.io.excel as excel
import packages.model.visco_plastic as visco_plastic
import packages.io.plotter as plotter

# Constants
DATA_PATH = './'
DATA_FILE = 'alloy_617'
PLOT_PATH = './results/'
PLOT_FILE = 'result_plot'
ALL_TEST_NAMES = ['G32', 'G33', 'G44', 'G25']
TRAIN_TEST_NAMES = ['G44', 'G25']

# Initialisation
start_time = time.time()
print('Program began on ' + time.strftime('%A, %D, %H:%M:%S', time.localtime()) + '!')

# Gets the experimental data
xl = excel.Excel(path = DATA_PATH, file = DATA_FILE)
exp_x_data = [xl.read_column(column = test_name + '_time', sheet = 'data') for test_name in ALL_TEST_NAMES]
exp_y_data = [xl.read_column(column = test_name + '_strain', sheet = 'data') for test_name in ALL_TEST_NAMES]
exp_stresses = xl.read_included('stress', ALL_TEST_NAMES)
print('The experimental data for ' + str(len(ALL_TEST_NAMES)) + ' test(s) has been read!')

# Prepare model and plotter
model = visco_plastic.ViscoPlastic(exp_stresses)
pt = plotter.Plotter(path = PLOT_PATH, plot = PLOT_FILE)
pt.prep_plot(title = 'Creep at 800°C', xlabel = 'Time (h)', ylabel = 'Creep Strain (%)')
pt.exp_plot(exp_x_data, exp_y_data)

# Get parameters
param_include_list = xl.read_column(column = 'include', sheet = 'vp_params')
params_list = [xl.read_column(column = param, sheet = 'vp_params') for param in model.params]
params_list = [[params[i] for params in params_list] for i in range(0, len(params_list[0]))] # transpose
params_list = [params_list[i] for i in range(0, len(params_list)) if int(param_include_list[i]) == 1]

# Conduct predictions
for params in params_list:
    prd_x_data, prd_y_data = model.get_prd_curves(*params)
    for i in range(0, len(prd_x_data)):
        if ALL_TEST_NAMES[i] in TRAIN_TEST_NAMES:
            pt.prd_plot([prd_x_data[i]], [prd_y_data[i]], 'b')
        else:
            pt.prd_plot([prd_x_data[i]], [prd_y_data[i]], 'r')

# Save plot and end
pt.save_plot()
print('Program finished on ' + time.strftime('%A, %D, %H:%M:%S', time.localtime()) + ' in ' + str(round(time.time()-start_time)) + ' seconds!')