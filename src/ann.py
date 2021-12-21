"""
 Title: An ANN for surrogate modeling
 Description: For creating the ANN surrogate model for the V-P model
 Author: Janzen Choi

"""

# General Libraries
from os import error
import pandas as pd
import numpy as np
import random 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import optimizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

# Custom Libraries
import package.io.excel as excel
import package.model.visco_plastic as visco_plastic
import package.objective as objective

# General Constants
INPUT_PATH     = './results/'
INPUT_FILE     = 'params_'
INPUT_SHEET    = 'params'
PARAMS          = visco_plastic.PARAMS
ERRORS          = objective.ERRORS

# ANN Constants
EPOCH = 500
BATCH_SIZE = 5
TRAIN_SIZE = 20000
TEST_SIZE = 1000

# Main function
def main():
    pass

# Defines the ANN model
def get_model():
    model = Sequential()
    model.add(Dense(units = len(PARAMS), activation = 'relu', input_dim = TRAIN_SIZE))
    model.add(Dense(units = 162*6, activation = 'relu'))
    model.add(Dense(units = 162*4, activation = 'relu'))
    model.add(Dense(units = 162*2, activation = 'relu'))
    model.add(Dense(units = 162, activation = 'relu'))
    model.add(Dense(units = 64, activation = 'relu'))
    model.add(Dense(units = 32, activation = 'relu'))
    model.add(Dense(units = 16, activation = 'relu'))
    model.add(Dense(units = len(ERRORS)))
    model.summary()
    return model
    
# Reads random parameters and errors
def read_io(num_samples, stresses):

    # Get data for each stress
    inputs_list, outputs_list = [], []
    for stress in stresses:

        # Read data corresponding to stress
        xl = excel.Excel(path = INPUT_PATH, file = INPUT_FILE + str(stress), sheet = INPUT_SHEET)
        
        # Gets all the parameters
        params_list = [xl.read_column(column=param) for param in PARAMS] # reads all the parameters
        params_list = [[param[i] for param in params_list] for i in range(0,len(params_list[0]))] # transposes

        # Gets all the errors
        errors_list = [xl.read_column(column=error) for error in ERRORS] # reads all the errors
        errors_list = [[error[i] for error in errors_list] for i in range(0,len(errors_list[0]))] # transposes
        
        # Samples randomly
        index_list = [random.randint(0, len(params_list)-1) for i in range(0, num_samples)]
        params_list = [params_list[i] for i in index_list]
        errors_list = [errors_list[i] for i in index_list]

        # Add to inputs/outputs list
        inputs_list.append(params_list)
        outputs_list.append(errors_list)

    # Return inputs and outputs
    return inputs_list, outputs_list

# Calls the main function
if __name__ == '__main__':
    main()