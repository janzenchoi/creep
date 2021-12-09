"""
 Title: Recorder
 Description: Specifically for recording data as the MOGA operates
 Author: Janzen Choi

"""

# Libraries
import plot
import excel
import numpy

# Constants
RECORD_INTERVAL = 10
POPULATION_LIMIT = 10
RESULTS_PATH     = '../results/'
RECORD_FILE_NAME = 'recorded_params'
RECORD_PLOT_NAME = 'recorded_curves'
TEXT_FILE_NAME   = 'summary'

# The Recorder class
class Recorder:

    # Constructor
    def __init__(self, model, obj, moga):
        self.model      = model
        self.params     = model.params
        self.errors     = obj.errors
        self.exp_x_data = obj.exp_x_data
        self.exp_y_data = obj.exp_y_data
        self.init_pop   = moga.init_pop
        self.offspring  = moga.offspring
        self.num_evals  = 0
        self.opt_params = []
        self.opt_errors = []

    # Maintains a sorted list of the top X optimal parameters 
    def update_population(self, params, err_list):
        params, err_list = list(params), list(err_list)
        err_total = numpy.average(err_list)
        
        # If the stored parameters exceed the limit, remove the worst
        if len(self.opt_params) == POPULATION_LIMIT:
            if self.opt_errors[-1][-1] < err_total:
                return
            self.opt_params.pop()
            self.opt_errors.pop()

        # Adds new params in order
        inserted = False
        for i in range(0, len(self.opt_params)):
            if err_total < self.opt_errors[i][-1]:
                self.opt_params.insert(i, params)
                self.opt_errors.insert(i, err_list + [err_total])
                inserted = True
                break

        # If new params is worst between existing params
        if not inserted:
            self.opt_params.append(params)
            self.opt_errors.append(err_list + [err_total])

    # Records the results
    def record_results(self):
        
        # Plot the optimal curves
        params = self.opt_params[0]
        prd_x_data, prd_y_data = self.model.get_prd_curves(*params)
        plot.prep_plot()
        plot.exp_plot(self.exp_x_data, self.exp_y_data)
        plot.prd_plot(prd_x_data, prd_y_data)
        plot.save_plot()

        # Writes the top X params and their errors
        data = []
        for i in range(0,len(self.opt_params)):
            data.append(self.opt_params[i] + self.opt_errors[i])
        data_names = self.params + self.errors + ['err_total']
        excel.write_columns(data, data_names)

    # Updates the record
    def update_record(self, params, err_list):
        
        # Updates the population
        self.update_population(params, err_list)

        # Only display record after X generations
        self.num_evals += 1
        num_gens = (self.num_evals - self.init_pop) / self.offspring
        if num_gens > 0 and num_gens % RECORD_INTERVAL == 0:
            
            # Gets the num_gens string
            num_gen_str = "(" + str(round(num_gens)) + ")"

            # Plot the optimal curves
            params = self.opt_params[0]
            prd_x_data, prd_y_data = self.model.get_prd_curves(*params)
            plot.prep_plot()
            plot.exp_plot(self.exp_x_data, self.exp_y_data)
            plot.prd_plot(prd_x_data, prd_y_data)
            plot.save_plot(RESULTS_PATH + RECORD_PLOT_NAME + " " + num_gen_str)

            # Writes the top X params and their errors
            data = [self.opt_params[i] + self.opt_errors[i] for i in range(0,len(self.opt_params))]
            data_names = self.params + self.errors + ['err_total']
            excel.write_columns(data, data_names, file_name = RESULTS_PATH + RECORD_FILE_NAME + " " + num_gen_str)

            # Writes the optimal results to a text file
            file = open(RESULTS_PATH + TEXT_FILE_NAME + '.txt', 'w')
            summary = 'gens : ' + str(round(num_gens)) + '\n'
            for i in range(0,len(data_names)):
                summary += data_names[i] + ' : ' + str(round(data[0][i], 5)) + '\n'
            file.write(summary)
            file.close()

            # Print out record message
            print("=======================================================")
            print("Recorded results " + num_gen_str)
            print("=======================================================")