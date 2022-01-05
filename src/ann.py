"""
 Title: An ANN for surrogate modeling
 Description: For creating the ANN surrogate model for the V-P model
 Author: Janzen Choi

"""

# General Libraries
import time
from tensorflow import keras
from tensorflow.keras import optimizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

# Custom Libraries
import packages.sampler as sampler
import packages.polyfier as polyfier
import packages.model.visco_plastic as visco_plastic

# Constants
PARAMS_LIST = visco_plastic.PARAMS
POLY_DEG    = polyfier.DEFAULT_POLY_DEG

# ANN Constants
NUM_EPOCHS  = 500
BATCH_SIZE  = 5
TRAIN_SIZE  = 5000
TEST_SIZE   = 1000
ACTIVATION  = 'relu'

# Initialisation
start_time = time.time()
print('ANN modelling has begun!')

# Prepare testing and training samples
sp = sampler.Sampler()
training_inputs, training_outputs = sp.sample(TRAIN_SIZE)
testing_inputs, testing_outputs = sp.sample(TEST_SIZE)
print('Samples read in and prepared!')

# Construct the model
model = Sequential()
model.add(Dense(units = len(training_inputs[0]), activation = ACTIVATION, input_dim = len(training_inputs[0])))
model.add(Dense(units = 162*6, activation = ACTIVATION))
model.add(Dense(units = 162*4, activation = ACTIVATION))
model.add(Dense(units = 162*2, activation = ACTIVATION))
model.add(Dense(units = 162, activation = ACTIVATION))
model.add(Dense(units = 64, activation = ACTIVATION))
model.add(Dense(units = 32, activation = ACTIVATION))
model.add(Dense(units = 16, activation = ACTIVATION))
model.add(Dense(units = len(training_outputs[0])))
model.summary()
print('Model has been created!')

# Define loss and optimisation methods
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
model.loss = 'mean_squared_error'
print('Optimisation has been set up!')

# Conduct the optimisation
xy_fit = model.fit(training_inputs, training_outputs, epochs = NUM_EPOCHS, batch_size = BATCH_SIZE, validation_data = (testing_inputs, testing_outputs), verbose=2)
print('ANN modelling has concluded!')

# End message
print('Program finished at ' + time.strftime('%H:%M:%S', time.localtime()) + ' in ' + str(round(time.time()-start_time)) + ' seconds!')