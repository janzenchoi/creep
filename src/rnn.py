"""
 Title: An ANN for surrogate modeling
 Description: For creating the ANN surrogate model for the V-P model
 Author: Janzen Choi

"""

# General Libraries
import time
import numpy as np
import tensorflow as tf
from keras.models import Model

# Custom Libraries
import packages.sampler as sampler
import packages.polyfier as polyfier
import packages.model.visco_plastic as visco_plastic

# Constants
PARAMS_LIST = visco_plastic.PARAMS
POLY_DEG    = polyfier.DEFAULT_POLY_DEG

# ANN Constants
LEARNING_RATE   = 0.001
NUM_EPOCHS      = 500
BATCH_SIZE      = 5
TRAIN_SIZE      = 5000
TEST_SIZE       = 1000
ACTIVATION      = 'relu'

# Initialisation
start_time = time.time()
print('ANN modelling has begun!')

# Prepare testing and training samples
sp = sampler.Sampler()
training_outputs, training_inputs = sp.sample(TRAIN_SIZE)
testing_outputs, testing_inputs = sp.sample(TEST_SIZE)
print('Samples read in and prepared!')

# Construct the model
optimiser = tf.keras.optimisers.Adam(learning_rate = )
print('Model has been created!')

# Define loss and optimisation methods

print('Optimisation has been set up!')

# Conduct the optimisation
xy_fit = model.fit(training_inputs, training_outputs, epochs = NUM_EPOCHS, batch_size = BATCH_SIZE, validation_data = (testing_inputs, testing_outputs), verbose=2)
print('ANN modelling has concluded!')

# End message
print('Program finished at ' + time.strftime('%H:%M:%S', time.localtime()) + ' in ' + str(round(time.time()-start_time)) + ' seconds!')

# model = keras.Sequential()
# model.add(layers.Embedding(input_dim = len(training_inputs[0]), output_dim = 64))
# model.add(layers.GRU(256, return_sequences=True))
# model.add(layers.SimpleRNN(128))
# model.add(layers.Dense(len(training_outputs[0])))
# model.summary()
# print('Model has been created!')

# # Define loss and optimisation methods
# model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
# model.loss = 'mean_squared_error'
# print('Optimisation has been set up!')