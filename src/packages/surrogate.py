"""
 Title: Surrogate Model
 Description: For creating the surrogate model
 Author: Janzen Choi

"""

# Libraries
import numpy as np
import pickle
from smt.surrogate_models import KPLS
import packages.io.plotter as plotter
import packages.polyfier as polyfier

# Constants
TRAINING_SAMPLES    = 273 # k^2 + 2*k + c_p (number of centre points)
TESTING_SAMPLES     = 10
MODEL_PATH          = './results/'
MODEL_FILE          = 'sm'

# Surrogate Model
class Surrogate:

    # Constructor
    def __init__(self):
        self.sm = KPLS(theta0=[1e-2]) # kriging model using partial least squares (PLS) 
        self.pf = polyfier.Polyfier()

    # Trains the surrogate model
    def train_sm(self, input_list, output_list):
        self.sm.set_training_values(np.array(input_list), np.array(output_list))
        self.sm.train()

    # Assesses the surrogate model
    def assess_sm(self, input_list, output_list):
        
        # Initialise
        prd_output_list = self.sm.predict_values(np.array(input_list))

        # Compare with expected output
        for i in range(0, len(input_list)):

            # Gets the expected y values
            exp_x_end  = output_list[i][0]
            exp_x_list = self.pf.get_x_list(exp_x_end)
            exp_y_list = output_list[i][1:]
            
            # Gets the expected and predicted y lists
            prd_x_end  = prd_output_list[i][0]
            prd_x_list = self.pf.get_x_list(prd_x_end)
            prd_y_list = prd_output_list[i][1:]

            # Gets the errors
            err_x_end = abs(exp_x_end - prd_x_end) / exp_x_end
            err_y_end = abs(exp_y_list[-1] - prd_y_list[-1]) / exp_y_list[-1]
            err_area = np.average([abs(exp_y_list[j] - prd_y_list[j]) / exp_y_list[j] for j in range(0, min(len(exp_y_list), len(prd_y_list)))])

            # Prints out the error
            print('[Test ' + str(i) + ']')
            print(' err_x_end = ' + str(round(err_x_end, 3)))
            print(' err_y_end = ' + str(round(err_y_end, 3)))
            print(' err_area  = ' + str(round(err_area, 3)))
            print()

            # Plots the curves
            plt = plotter.Plotter(MODEL_PATH, 'sm_' + str(i))
            plt.prep_plot()
            plt.exp_plot([exp_x_list], [exp_y_list])
            plt.prd_plot([prd_x_list], [prd_y_list])
            plt.save_plot()

    # Saves the trained model (via pickling)
    def save_sm(self):
        with open(MODEL_PATH + MODEL_FILE + ".pkl", "wb") as f:
            pickle.dump(self.sm, f)

    # Loads the trained model (via pickling)
    def load_sm(self):
        with open(MODEL_PATH + MODEL_FILE + ".pkl", "rb") as f:
            self.sm = pickle.load(f)