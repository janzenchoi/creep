"""
 Title: Recorder
 Description: For recording results periodically
 Author: Janzen Choi

"""

# Libraries
import time, math
import numpy as np
import pandas as pd
from itertools import zip_longest


# Constants
RECORD_INTERVAL = 1
POPULATION_LIMIT = 50
DEFAULT_PATH = './'
CURVE_DENSITY = 100

# The recorder class
class Recorder:

    # Constructor
    def __init__(self, identifier, model, obj_func, settings, path = DEFAULT_PATH):

        # Set up writer
        self.identifier_string = str(identifier).zfill(3) # supports 0-999
        self.filename = 'results_' + self.identifier_string
        self.path = path
        
        # Record settings
        self.model_name = settings['model']
        self.test_names = settings['tests']
        self.error_names = settings['errors']
        self.moga_options = settings['moga']
    
        # Model
        self.model = model

        # Experimental data
        exp_x_data = [get_thinned_list(exp_x_list) for exp_x_list in obj_func.exp_x_data]
        exp_y_data = [get_thinned_list(exp_y_list) for exp_y_list in obj_func.exp_y_data]
        self.exp_x_flat = [exp_x for exp_x_list in exp_x_data for exp_x in exp_x_list] # flatten
        self.exp_y_flat = [exp_y for exp_y_list in exp_y_data for exp_y in exp_y_list] # flatten

        # Track optimisation progress
        self.start_time = time.time()
        self.start_time_str = time.strftime('%A, %D, %H:%M:%S', time.localtime())
        self.num_evals  = 0
        self.num_gens   = 0
        self.opt_params = []
        self.opt_errors = []

    # Updates the optimal population
    def update_population(self, params, errors):
        params, errors = list(params), list(errors)
        error_avg = np.average(errors)

        # If the stored parameters exceed the limit, remove the worst
        if len(self.opt_params) == POPULATION_LIMIT:
            if self.opt_errors[-1][-1] < error_avg:
                return
            self.opt_params.pop()
            self.opt_errors.pop()
        
        # Adds new params in order
        inserted = False
        for i in range(0, len(self.opt_params)):
            if error_avg < self.opt_errors[i][-1]:
                self.opt_params.insert(i, params)
                self.opt_errors.insert(i, errors + [error_avg])
                inserted = True
                break

        # If new params is worst between existing params
        if not inserted:
            self.opt_params.append(params)
            self.opt_errors.append(errors + [error_avg])

    # Updates the results after X iterations
    def update_results(self, params, errors):

        # Updates the population
        self.update_population(params, errors)

        # Update optimisation progress
        self.num_evals += 1
        self.num_gens = (self.num_evals - self.moga_options['init_pop']) / self.moga_options['offspring'] + 1
        
        # Record results after X iterations
        if self.num_gens > 0 and self.num_gens % RECORD_INTERVAL == 0:
            progress = str(round(self.num_gens)) + '/' + str(self.moga_options['num_gens'])
            writer = pd.ExcelWriter(self.path + self.filename + '.xlsx', engine='xlsxwriter')
            self.record_settings(writer)
            self.record_results(writer)
            self.record_plot(writer)
            writer.save()
            print('[' + self.identifier_string + ']: Recorded results (' + progress + ')')
            # try:
            #     print('[' + self.identifier_string + ']: Recorded results (' + progress + ')')
            # except:
            #     print('[' + self.identifier_string + ']: Failed to record results (' + progress + ')')

    # Records the settings
    def record_settings(self, writer):
        columns = [
            'Status', 'Progress', 'Start Time', 'End Time', 'Time Elapsed', 'Model', 'Params', 'Tests', 'Errors',
            'num_gens', 'init_pop', 'offspring', 'crossover', 'mutation'
        ]

        # Prepare data
        status = 'Complete' if self.num_gens == self.moga_options['num_gens'] else 'Incomplete'
        progress = str(round(self.num_gens)) + '/' + str(self.moga_options['num_gens'])
        time_elapsed = str(round(time.time() - self.start_time)) + 's'
        data = zip_longest(
            [status], [progress], [self.start_time_str], [time.strftime('%A, %D, %H:%M:%S', time.localtime())],
            [time_elapsed], [self.model_name], self.model.params, self.test_names, self.error_names,
            [self.moga_options['num_gens']], [self.moga_options['init_pop']], [self.moga_options['offspring']],
            [self.moga_options['crossover']], [self.moga_options['mutation']]
        )
        settings = pd.DataFrame([d for d in data], columns=columns)

        # Write settings
        settings.style.apply(centre_align, axis = 0).to_excel(writer, 'settings', index = False)
        sheet = writer.sheets['settings']
        for column in settings:
            column_length = max(settings[column].astype(str).map(len).max(), len(column)) + 1
            column_index = settings.columns.get_loc(column)
            sheet.set_column(column_index, column_index, column_length)

    # Records the results
    def record_results(self, writer):
        columns = self.model.params + self.error_names + ['err_avg']
        data = [self.opt_params[i] + self.opt_errors[i] for i in range(0,len(self.opt_params))]
        results = pd.DataFrame(data, columns=columns)
        results.to_excel(writer, 'results', index = False)

    # Records the plot
    def record_plot(self, writer):

        # Prepare predicted curves
        prd_x_data, prd_y_data = self.model.get_prd_curves(*self.opt_params[0])
        prd_x_flat = [prd_x for prd_x_list in prd_x_data for prd_x in get_thinned_list(prd_x_list)] # flatten
        prd_y_flat = [prd_y for prd_y_list in prd_y_data for prd_y in get_thinned_list(prd_y_list)] # flatten
        
        # Prepare chart
        data = zip_longest(self.exp_x_flat, self.exp_y_flat, prd_x_flat, prd_y_flat)
        pd.DataFrame(data).to_excel(writer, 'plot', index = False)
        workbook = writer.book
        worksheet = writer.sheets['plot']
        chart = workbook.add_chart({'type': 'scatter'})

        # Add curves to chart
        marker = {'type': 'circle', 'size': 3}
        chart.add_series({'categories': ['plot', 1, 0, len(prd_x_flat), 0], 'values': ['plot', 1, 1, len(prd_x_flat), 1], 'marker': marker})
        chart.add_series({'categories': ['plot', 1, 2, len(prd_x_flat), 2], 'values': ['plot', 1, 3, len(prd_x_flat), 3], 'marker': marker})

        # Insert chart into worksheet
        chart.set_x_axis({'name': 'Time', 'major_gridlines': {'visible': True}})
        chart.set_y_axis({'name': 'Strain', 'major_gridlines': {'visible': True}})
        worksheet.insert_chart('A1', chart)

# For centre-aligning the cellss
def centre_align(x):
    return ['text-align: center' for _ in x]

# Returns a thinned list
def get_thinned_list(unthinned_list):
    src_data_size = len(unthinned_list)
    step_size = src_data_size / CURVE_DENSITY
    thin_indexes = [math.floor(step_size*i) for i in range(1, CURVE_DENSITY - 1)]
    thin_indexes = [0] + thin_indexes + [src_data_size - 1]
    return [unthinned_list[i] for i in thin_indexes]