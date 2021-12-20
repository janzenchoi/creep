"""
 Title: Surrogate Model
 Description: For creating the surrogate model for the V-P model
 Author: Janzen Choi

"""

# Libraries
import time
import random
import numpy as np
import pickle
import package.io.excel as excel
import package.model.visco_plastic as visco_plastic
import package.objective as objective
from smt.sampling_methods import LHS
from smt.surrogate_models import KPLS

# Constants
TRAINING_SAMPLES    = 273 # k^2 + 2*k + c_p (number of centre points)
TESTING_SAMPLES     = 100
MODEL_PATH          = './results/'
MODEL_FILE          = 'sm'
DATA_PATH           = './'
DATA_FILE           = 'alloy_617'

# Main function
def main():

    # Initialisation
    start_time = time.time()
    print('Surrogate modeling has begun!')

    # Gets the experimental data
    xl = excel.Excel(path = DATA_PATH, file = DATA_FILE)
    test_names = xl.read_included('test')
    exp_x_data = [xl.read_column(column = test_name + '_time', sheet = 'data') for test_name in test_names]
    exp_y_data = [xl.read_column(column = test_name + '_strain', sheet = 'data') for test_name in test_names]
    exp_stresses = xl.read_included('stress')
    print('The experimental data for ' + str(len(test_names)) + ' test(s) has been read!')

    # Initialise everything
    model = visco_plastic.ViscoPlastic(exp_stresses)
    obj = objective.Objective(model, exp_x_data, exp_y_data)
    sg = Surrogate(model, obj)
    print('The surrogate model training has been prepared!')

    # Train the model
    training_params = get_params_list(sg.bounds, TRAINING_SAMPLES)
    training_errors = sg.get_errors(training_params)
    sg.train_sm(training_params, training_errors)
    print('The surrogate model has been trained!')

    # Save the model
    sg.save_sm()
    print('The surrogate model has been saved!')

    # Assesses the surrogate model predictions
    testing_params = get_params_list(sg.bounds, TESTING_SAMPLES)
    sg.assess_sm(testing_params)
    print('The surrogate model has been assessed!')

    # End message
    print('Surrogate modeling has finished in '+str(round(time.time()-start_time))+' seconds!')

# Surrogate Model
class Surrogate:

    # Constructor
    def __init__(self, model, obj):
        self.model = model
        self.obj = obj
        self.bounds = [[model.l_bnds[i],  model.u_bnds[i]] for i in range(0,len(model.l_bnds))]
        self.sample = LHS(xlimits = np.array(self.bounds))
        self.sm = KPLS(theta0=[1e-2]) # kriging model using partial least squares (PLS) 
        
    # Returns the errors from a list of parameters
    def get_errors(self, params_list):
        errors_list = [self.obj.get_errors(params) for params in params_list]
        return errors_list

    # Gets a list of parameter samples
    def get_params(self, size):
        params_list = []
        while len(params_list) < size:
            temp_params_list = self.sample(size)
            for params in temp_params_list:
                if np.average(self.obj.get_errors(params)) < 100:
                    params_list.append(params)
                if len(params_list) >= size:
                    break
            print('Parameters obtained: ' + str(len(params_list)) + '/' + str(size))
        return params_list

    # Trains the surrogate model
    def train_sm(self, inputs, outputs):
        self.sm.set_training_values(np.array(inputs), np.array(outputs))
        self.sm.train()

    # Assesses the surrogate model
    def assess_sm(self, testing_params):
        
        # Gets the errors
        predicted_errors = self.sm.predict_values(np.array(testing_params))
        actual_errors = self.get_errors(testing_params)

        # Prints out the results
        all_re = [[] for i in range(0, len(self.obj.errors))]
        for i in range(0, len(predicted_errors)):
            for j in range(0, len(predicted_errors[0])):
                re = round(abs(predicted_errors[i][j] - actual_errors[i][j]) / actual_errors[i][j], 3)
                print('(' + str(i) + ',' + str(j) + ') ' + str(self.obj.errors[j]) + ': ' + str(re))
                all_re[j].append(re)
        all_re = [np.average(diff) for diff in all_re]
        print('Average Errors: ' + str(all_re))

    # Saves the trained model (via pickling)
    def save_sm(self):
        with open(MODEL_PATH + MODEL_FILE + ".pkl", "wb") as f:
            pickle.dump(self.sm, f)

    # Loads the trained model (via pickling)
    def load_sm(self):
        with open(MODEL_PATH + MODEL_FILE + ".pkl", "rb") as f:
            self.sm = pickle.load(f)

# Generates a list of randomised parameters in given bounds
def get_params_list(bounds, num_params):
    params_list = []
    for i in range(0,num_params):
        params_list.append([random.uniform(bounds[j][0], bounds[j][1]) for j in range(0,len(bounds))])
    return params_list

# Calls the main function
if __name__ == '__main__':
    main()