"""
 Title: Recorder
 Description: Specifically for recording results as the MOGA operates
 Author: Janzen Choi

"""

# Libraries
import packages.io.plotter as plotter
import packages.io.excel as excel
import packages.io.tracker as tracker
import time
import numpy as np

# Constants
RECORD_INTERVAL = 10
POPULATION_LIMIT = 50
DEFAULT_PATH = './'
DEFAULT_FOLDER = 'folder'
RECORD_FILE_NAME = 'params'
RECORD_PLOT_NAME = 'curves'
TEXT_FILE_NAME   = 'summary'

# The Recorder class
class Recorder:

    # Constructor
    def __init__(self, model, obj, moga, path = DEFAULT_PATH, folder = DEFAULT_FOLDER):
        
        # Optimisation information
        self.model      = model
        self.params     = model.params
        self.errors     = obj.errors
        self.exp_x_data = obj.exp_x_data
        self.exp_y_data = obj.exp_y_data

        # MOGA information
        self.num_gens   = moga.num_gens
        self.init_pop   = moga.init_pop
        self.offspring  = moga.offspring
        self.crossover  = moga.crossover
        self.mutation   = moga.mutation
        
        # Tracking optimisation progress
        self.start_time = time.time()
        self.start_time_str = time.strftime('%A, %D, %H:%M:%S', time.localtime())
        self.num_evals  = 0
        self.opt_params = []
        self.opt_errors = []

        # Summarise optimisation settings
        self.settings = self.get_settings()

        # For tracking the directory
        tr = tracker.Tracker(path, folder)
        tr.create_directory()
        self.path_folder = tr.get_path_folder()

    # Prepare optimisation settings
    def get_settings(self):
        settings = '[Optimisation Settings]:\n'
        settings += ' params    = ' + str(self.model.params) + '\n'
        settings += ' l_bnds    = ' + str(self.model.l_bnds) + '\n'
        settings += ' u_bnds    = ' + str(self.model.u_bnds) + '\n'
        settings += ' stresses  = ' + str(self.model.stresses) + '\n'
        settings += ' errors    = ' + str(self.errors) + '\n'
        settings += ' num_gens  = ' + str(self.num_gens) + '\n'
        settings += ' init_pop  = ' + str(self.init_pop) + '\n'
        settings += ' offspring = ' + str(self.offspring) + '\n'
        settings += ' crossover = ' + str(self.crossover) + '\n'
        settings += ' mutation  = ' + str(self.mutation) + '\n'
        return settings

    # Maintains a sorted list of the top X optimal parameters 
    def update_population(self, params, err_list):
        params, err_list = list(params), list(err_list)
        err_avg = np.average(err_list)
        
        # If the stored parameters exceed the limit, remove the worst
        if len(self.opt_params) == POPULATION_LIMIT:
            if self.opt_errors[-1][-1] < err_avg:
                return
            self.opt_params.pop()
            self.opt_errors.pop()

        # Adds new params in order
        inserted = False
        for i in range(0, len(self.opt_params)):
            if err_avg < self.opt_errors[i][-1]:
                self.opt_params.insert(i, params)
                self.opt_errors.insert(i, err_list + [err_avg])
                inserted = True
                break

        # If new params is worst between existing params
        if not inserted:
            self.opt_params.append(params)
            self.opt_errors.append(err_list + [err_avg])

    # Updates the summary file of the optimisation
    def update_summary(self):

        # Summarise optimisation progress
        progress = '[Optimisation Progress]:\n'
        progress += ' start_time   = ' + self.start_time_str + '\n'
        progress += ' last_updated = ' + time.strftime('%A, %D, %H:%M:%S', time.localtime()) + '\n'
        progress += ' time_elapsed = ' + str(round(time.time()-self.start_time)) + 's' + '\n'

        # Summarise optimisation results
        data_names = self.params + self.errors + ['err_avg']
        num_gens = (self.num_evals - self.init_pop) / self.offspring
        results = '[Optimisation Results]:\n'
        results += ' gens = ' + str(round(num_gens)) + '\n'
        data = self.opt_params[0] + self.opt_errors[0]
        for i in range(0,len(data_names)):
            results += ' ' + data_names[i] + ' = ' + str(round(data[i], 5)) + '\n'

        # Write summaries
        file = open(self.path_folder + TEXT_FILE_NAME + '.txt', 'w')
        file.write(self.settings + '\n' + progress + '\n' + results)
        file.close()

    # Updates the record
    def update_record(self, params, err_list):
        
        # Updates the population
        self.update_population(params, err_list)

        # Get number of generations passed
        self.num_evals += 1
        num_gens = (self.num_evals - self.init_pop) / self.offspring

        # At each generation, write the optimal results to a text file
        if num_gens > 0 and num_gens % 1 == 0:
            self.update_summary()

        # After X number of generations, plot and write top results
        if num_gens > 0 and num_gens % RECORD_INTERVAL == 0:

            # Plot the optimal curves
            params = self.opt_params[0]
            prd_x_data, prd_y_data = self.model.get_prd_curves(*params)
            pt = plotter.Plotter(path = self.path_folder, plot = RECORD_PLOT_NAME + " " + "(" + str(round(num_gens)) + ")")
            pt.prep_plot()
            pt.exp_plot(self.exp_x_data, self.exp_y_data)
            pt.prd_plot(prd_x_data, prd_y_data)
            pt.save_plot()

            # Writes the top X params and their errors
            data = [self.opt_params[i] + self.opt_errors[i] for i in range(0,len(self.opt_params))]
            data_names = self.params + self.errors + ['err_avg']
            xl = excel.Excel(path = self.path_folder, file = RECORD_FILE_NAME + " " + "(" + str(round(num_gens)) + ")", sheet = 'params')
            xl.write_data(data, data_names)

            