"""
 Title: Surrogate Model
 Description: For creating the surrogate model for the V-P model
 Author: Janzen Choi

"""

# Libraries
from math import e
import time
import random
import numpy as np
import pickle
import packages.io.excel as excel
import packages.io.plotter as plotter
import packages.model.visco_plastic as visco_plastic
import packages.objective as objective
import packages.polyfier as polyfier
from smt.surrogate_models import KPLS

# Constants
TRAINING_SAMPLES    = 273 # k^2 + 2*k + c_p (number of centre points)
TESTING_SAMPLES     = 10
STRESS              = 80
MODEL_PATH          = './results/'
MODEL_FILE          = 'sm_' + str(STRESS)
INPUT_PATH          = './results/'
INPUT_FILE          = 'good_params_' + str(STRESS)
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

            # Gets the expected and predicted y lists
            exp_y_list = polyfier.process(output_list[i])
            prd_y_list = polyfier.process(prd_output_list[i])

            # Gets the errors
            err_x_end = abs(len(exp_y_list) - len(prd_y_list)) / len(exp_y_list)
            err_y_end = abs(exp_y_list[-1] - prd_y_list[-1]) / exp_y_list[-1]
            err_area = np.average([abs(exp_y_list[j] - prd_y_list[j]) / exp_y_list[j] for j in range(0, min(len(exp_y_list), len(prd_y_list)))])

            # Prints out the error
            print('[Test ' + str(i) + ']')
            print('  err_x_end = ' + str(round(err_x_end, 3)))
            print('  err_y_end = ' + str(round(err_y_end, 3)))
            print('  err_area  = ' + str(round(err_area, 3)))
            print()

            # Plots the curves
            plt = plotter.Plotter(MODEL_PATH, 'sm_' + str(i))
            plt.prep_plot()
            plt.exp_plot([polyfier.get_x_list(exp_y_list)], [exp_y_list])
            plt.prd_plot([polyfier.get_x_list(prd_y_list)], [prd_y_list])
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
        print('  avg_err_x_end = ' + str(round(avg_err_x_end, 3)))
        print('  avg_err_y_end = ' + str(round(avg_err_y_end, 3)))
        print('  avg_err_area  = ' + str(round(avg_err_area, 3)))
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
        self.params_list = [xl.read_column(column = params) for params in PARAMS]
        self.params_list = [[params[i] for params in self.params_list] for i in range(0,len(self.params_list[0]))] # transposes

        # Gets the list of end-points
        x_end_list = xl.read_column(column = 'x_end')
        
        # Gets the list of polynomials
        coefficients = ['c_' + str(term) for term in range(0, polyfier.POLY_DEG+1)]
        polynomial_list = [xl.read_column(column = coefficient) for coefficient in coefficients]
        polynomial_list = [[polynomial[i] for polynomial in polynomial_list] for i in range(0,len(polynomial_list[0]))] # transposes

        # Gets the list of y values (outputs)
        self.y_list_list = []
        for i in range(0, len(self.params_list)):
            _, y_list = polyfier.polynomial_to_curve(x_end_list[i], polynomial_list[i])
            self.y_list_list.append(y_list)

    # Reads random parameters and errors
    def sample(self, num_samples):
        index_list  = [random.randint(0, len(self.params_list) - 1) for i in range(0, num_samples)]
        input_list = [self.params_list[i] for i in index_list]
        output_list  = [self.y_list_list[i] for i in index_list]
        return input_list, output_list

# Calls the main function
if __name__ == '__main__':
    main()

# # Assesses the surrogate model
# def assess_sm(self, input_list, output_list):
    
#     # Gets the predicted output of the SM
#     prd_output_list = self.sm.predict_values(np.array(input_list))

#     # Initialise average error
#     avg_err_x_end, avg_err_y_end, avg_err_area = 0, 0, 0

#     # Compare with expected output
#     for i in range(0, len(input_list)):

#         # Gets the end point expected curve
#         exp_x_end = output_list[i][0]
#         exp_polynomial = output_list[i][1:]
#         exp_y_end = list(np.polyval(exp_polynomial, [exp_x_end]))[0]
        
#         # Gets the end point of the predicted curve
#         prd_x_end = prd_output_list[i][0]
#         prd_polynomial = prd_output_list[i][1:]
#         prd_y_end = list(np.polyval(prd_polynomial, [prd_x_end]))[0]

#         # Compare end points of curves
#         err_x_end = abs(exp_x_end - prd_x_end) / exp_x_end
#         err_y_end = abs(exp_y_end - prd_y_end) / exp_y_end
        
#         # Gets the area between the two curves
#         min_x_end = min(exp_x_end, prd_x_end)
#         _, exp_y_list = polyfier.polynomial_to_curve(min_x_end, exp_polynomial)
#         _, prd_y_list = polyfier.polynomial_to_curve(min_x_end, prd_polynomial)
#         err_area = np.average([abs(exp_y_list[j] - prd_y_list[j]) / exp_y_list[j] for j in range(0, len(exp_y_list))])

#         # Prints out the error
#         print('[Test ' + str(i) + ']')
#         print('  err_x_end = ' + str(round(err_x_end, 3)))
#         print('  err_y_end = ' + str(round(err_y_end, 3)))
#         print('  err_area  = ' + str(round(err_area, 3)))
#         print()

#         # Plots the curves
#         exp_x_list, exp_y_list = polyfier.polynomial_to_curve(exp_x_end, exp_polynomial)
#         prd_x_list, prd_y_list = polyfier.polynomial_to_curve(prd_x_end, prd_polynomial)
#         plt = plotter.Plotter(MODEL_PATH, 'sm_' + str(i))
#         plt.prep_plot()
#         plt.exp_plot([exp_x_list], [exp_y_list])
#         plt.prd_plot([prd_x_list], [prd_y_list])
#         plt.save_plot()

#         # Add error to average
#         avg_err_x_end += err_x_end
#         avg_err_y_end += err_y_end
#         avg_err_area += err_area

#     # Calculate average error
#     avg_err_x_end /= len(input_list)
#     avg_err_y_end /= len(input_list)
#     avg_err_area /= len(input_list)

#     # Display average error
#     print('[Summary]')
#     print('  avg_err_x_end = ' + str(round(avg_err_x_end, 3)))
#     print('  avg_err_y_end = ' + str(round(avg_err_y_end, 3)))
#     print('  avg_err_area  = ' + str(round(avg_err_area, 3)))
#     print()