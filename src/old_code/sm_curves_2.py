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
import packages.io.excel as excel
import packages.io.plotter as plotter
import packages.model.visco_plastic as visco_plastic
import packages.objective as objective
from smt.surrogate_models import KPLS

# Constants
TRAINING_SAMPLES    = 1273 # k^2 + 2*k + c_p (number of centre points)
TESTING_SAMPLES     = 10
STRESS              = 80
NUM_POINTS          = 50
POLY_DEG            = 15
MODEL_PATH          = './results/'
MODEL_FILE          = 'sm_' + str(STRESS)
INPUT_PATH          = './results/'
INPUT_FILE          = 'wide_80_15'
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
    print('The surrogate model has been trained with ' + str(TRAINING_SAMPLES) + ' samples!')

    # Save the model
    sg.save_sm()
    print('The surrogate model has been saved!')

    # Assesses the surrogate model predictions
    testing_inputs, testing_outputs = sampler.sample(TESTING_SAMPLES)
    sg.assess_sm(testing_inputs, testing_outputs)
    print('The surrogate model has been assessed with ' + str(TESTING_SAMPLES) + ' samples!')

    # End message
    print('Surrogate modeling has finished in '+str(round(time.time()-start_time))+' seconds!')

# Surrogate Model
class Surrogate:

    # Constructor
    def __init__(self):
        self.sm = KPLS(theta0=[1e-2]) # kriging model using partial least squares (PLS) 

    # Trains the surrogate model
    def train_sm(self, input_list, output_list):
        self.sm.set_training_values(np.array(input_list), np.array(output_list))
        self.sm.train()

    # Assesses the surrogate model
    def assess_sm(self, input_list, output_list):
        
        # Gets the predicted output of the SM
        prd_output_list = self.sm.predict_values(np.array(input_list))

        # Initialise average error
        avg_err_x_end, avg_err_y_end, avg_err_area = 0, 0, 0

        # Compare with expected output
        for i in range(0, len(input_list)):

            # Gets the expected y values
            exp_x_end = output_list[i][0]
            exp_x_list = np.linspace(0, exp_x_end, NUM_POINTS, endpoint = True)
            exp_y_list = output_list[i][1:]
            
            # Gets the expected and predicted y lists
            prd_x_end = prd_output_list[i][0]
            prd_x_list = np.linspace(0, prd_x_end, NUM_POINTS, endpoint = True)
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

            # Add error to average
            avg_err_x_end += err_x_end
            avg_err_y_end += err_y_end
            avg_err_area += err_area

        # Calculate average error
        avg_err_x_end /= len(input_list)
        avg_err_y_end /= len(input_list)
        avg_err_area /= len(input_list)

        # Display average error
        print('[Summary]')
        print(' avg_err_x_end = ' + str(round(avg_err_x_end, 3)))
        print(' avg_err_y_end = ' + str(round(avg_err_y_end, 3)))
        print(' avg_err_area  = ' + str(round(avg_err_area, 3)))
        print()

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

        # Prepare excel reader/writer
        xl = excel.Excel(path = INPUT_PATH, file = INPUT_FILE, sheet = INPUT_SHEET)
        
        # Gets the list of parameters (inputs)
        self.input_list = [xl.read_column(column = params) for params in PARAMS]
        self.input_list = [[input[i] for input in self.input_list] for i in range(0,len(self.input_list[0]))] # transposes

        # Gets the list of end-points
        x_end_list = xl.read_column(column = 'x_end')
        
        # Gets the list of polynomials
        coefficients = ['c_' + str(term) for term in range(0, POLY_DEG+1)]
        polynomial_list = [xl.read_column(column = coefficient) for coefficient in coefficients]
        polynomial_list = [[polynomial[i] for polynomial in polynomial_list] for i in range(0,len(polynomial_list[0]))] # transposes

        # Gets the list of end points and y values (outputs)
        self.output_list = []
        for i in range(0, len(self.input_list)):
            x_list = np.linspace(0, x_end_list[i], NUM_POINTS, endpoint = True)
            y_list = list(np.polyval(polynomial_list[i], x_list))
            output = [x_end_list[i]] + y_list
            self.output_list.append(output)

    # Reads random parameters and errors
    def sample(self, num_samples):
        index_list  = [random.randint(0, len(self.input_list) - 1) for i in range(0, num_samples)]
        input_list = [self.input_list[i] for i in index_list]
        output_list  = [self.output_list[i] for i in index_list]
        return input_list, output_list

# Calls the main function
if __name__ == '__main__':
    main()