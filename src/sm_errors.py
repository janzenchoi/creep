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
from smt.surrogate_models import KPLS

# Constants
TRAINING_SAMPLES    = 273 # k^2 + 2*k + c_p (number of centre points)
TESTING_SAMPLES     = 100
STRESS              = 60
MODEL_PATH          = './results/'
MODEL_FILE          = 'sm_' + str(STRESS)
INPUT_PATH          = './results/'
INPUT_FILE          = 'params_' + str(STRESS)
INPUT_SHEET         = 'params'
PARAMS              = visco_plastic.PARAMS
ERRORS              = objective.ERRORS

# Main function
def main():

    # Initialisation
    start_time = time.time()
    print('Surrogate modeling has begun!')

    # Prepare surrogate model and sampler
    sg = Surrogate()
    sampler = Sampler()
    print('Samples read in and prepared!')

    # Train the model
    training_inputs, training_outputs = sampler.sample(TRAINING_SAMPLES)
    sg.train_sm(training_inputs, training_outputs)
    print('The surrogate model has been trained!')

    # Save the model
    sg.save_sm()
    print('The surrogate model has been saved!')

    # Assesses the surrogate model predictions
    testing_inputs, testing_outputs = sampler.sample(TRAINING_SAMPLES)
    sg.assess_sm(testing_inputs, testing_outputs)
    print('The surrogate model has been assessed!')

    # End message
    print('Surrogate modeling has finished in '+str(round(time.time()-start_time))+' seconds!')

# Surrogate Model
class Surrogate:

    # Constructor
    def __init__(self):
        self.sm = KPLS(theta0=[1e-2]) # kriging model using partial least squares (PLS) 

    # Trains the surrogate model
    def train_sm(self, inputs, outputs):
        self.sm.set_training_values(np.array(inputs), np.array(outputs))
        self.sm.train()

    # Assesses the surrogate model
    def assess_sm(self, inputs, outputs):
        
        # Gets the errors
        predicted_outputs = self.sm.predict_values(np.array(inputs))

        # Prints out the results
        relative_error_list = [[] for i in range(0, len(ERRORS))]
        for i in range(0, len(predicted_outputs)):
            for j in range(0, len(predicted_outputs[0])):
                relative_error = round(abs(predicted_outputs[i][j] - outputs[i][j]) / outputs[i][j], 3)
                print('(' + str(i) + ',' + str(j) + ') ' + str(ERRORS[j]) + ': ' + str(relative_error))
                relative_error_list[j].append(relative_error)
        relative_error_list = [np.average(re) for re in relative_error_list]
        print('Average Errors: ' + str(relative_error_list))

    # Saves the trained model (via pickling)
    def save_sm(self):
        with open(MODEL_PATH + MODEL_FILE + ".pkl", "wb") as f:
            pickle.dump(self.sm, f)

    # Loads the trained model (via pickling)
    def load_sm(self):
        with open(MODEL_PATH + MODEL_FILE + ".pkl", "rb") as f:
            self.sm = pickle.load(f)

# For sampling parameters
class Sampler:

    # Constructor
    def __init__(self):
        
        # Get excel object
        xl = excel.Excel(path = INPUT_PATH, file = INPUT_FILE, sheet = INPUT_SHEET)
        
        # Gets all the parameters
        self.params_list = [xl.read_column(column=param) for param in PARAMS] # reads all the parameters
        self.params_list = [[param[i] for param in self.params_list] for i in range(0,len(self.params_list[0]))] # transposes

        # Gets all the errors
        self.errors_list = [xl.read_column(column=error) for error in ERRORS] # reads all the errors
        self.errors_list = [[error[i] for error in self.errors_list] for i in range(0,len(self.errors_list[0]))] # transposes

    # Reads random parameters and errors
    def sample(self, num_samples):
        
        # Samples randomly
        params_list, errors_list = [], []
        for i in range(0, num_samples):
            index = random.randint(0, len(self.params_list) - 1)
            if np.average(self.errors_list[index]) > 1:
                i -= 1
                continue
            params_list.append(self.params_list[index])
            errors_list.append(self.errors_list[index])

        # Returns params and errors
        return params_list, errors_list

# Calls the main function
if __name__ == '__main__':
    main()