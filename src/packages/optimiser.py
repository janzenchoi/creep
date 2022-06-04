"""
 Title: Optimiser
 Description: The optimiser which combines the model and MOGA
 Author: Janzen Choi

"""

# Libraries
import packages.io.excel as excel
import packages.io.recorder as recorder
import packages.model.visco_plastic as visco_plastic
import packages.error.objective as objective
import packages.genetic_algorithm as genetic_algorithm
from threading import Thread

# For conducting the optimisation
class Optimiser(Thread):

    # Constructor
    def __init__(self, settings, identifier, data_path = './', data_file = 'data', record_path = './'):
        Thread.__init__(self)
        self.settings = settings
        self.identifier = identifier
        self.data_path = data_path
        self.data_file = data_file
        self.record_path = record_path

    # Starts the optimisation
    def run(self):
        
        # Get information about the settings
        model_name = self.settings['model']
        test_names = self.settings['tests']
        error_names = self.settings['errors']
        moga_options = self.settings['moga']

        # Gets the experimental data
        xl = excel.Excel(path = self.data_path, file = self.data_file)
        exp_x_data = [xl.read_column(column = test_name + '_time', sheet = 'data') for test_name in test_names]
        exp_y_data = [xl.read_column(column = test_name + '_strain', sheet = 'data') for test_name in test_names]
        exp_stresses = xl.read_included('stress', test_names)

        # Define model
        available_models = [
            visco_plastic.ViscoPlastic(exp_stresses)
        ]
        model = [available_model for available_model in available_models if available_model.name == model_name][0]

        # Define optimiser
        obj_func = objective.Objective(error_names, exp_x_data, exp_y_data)
        moga = genetic_algorithm.MOGA(model, obj_func, moga_options['num_gens'], moga_options['init_pop'], moga_options['offspring'], moga_options['crossover'], moga_options['mutation'])

        # Define recorder
        rec = recorder.Recorder(self.identifier, model, obj_func, self.settings, path = self.record_path)
        moga.set_recorder(rec)

        # Conducts the optimisation
        print('[' + str(self.identifier).zfill(3) + ']: Commenced optimisation')
        moga.optimise()
        print('[' + str(self.identifier).zfill(3) + ']: Finished optimisation')