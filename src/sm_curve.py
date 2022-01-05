"""
 Title: Surrogate modeller
 Description: For creating the surrogate model for the V-P model
 Author: Janzen Choi

"""

# Libraries
import time
import packages.surrogate as surrogate
import packages.sampler as sampler

# Constants
TRAINING_SAMPLES    = surrogate.TRAINING_SAMPLES
TESTING_SAMPLES     = surrogate.TESTING_SAMPLES
STRESS              = 80

# Initialisation
start_time = time.time()
print('Surrogate modeling has begun!')

# Prepare surrogate model and sampler
sg = surrogate.Surrogate()
sp = sampler.Sampler()
print('Samples read in and prepared!')

# Train the model
training_inputs, training_outputs = sp.sample(TRAINING_SAMPLES)
sg.train_sm(training_inputs, training_outputs)
print('The surrogate model has been trained with ' + str(TRAINING_SAMPLES) + ' samples!')

# Save the model
sg.save_sm()
print('The surrogate model has been saved!')

# Assesses the surrogate model predictions
testing_inputs, testing_outputs = sp.sample(TESTING_SAMPLES)
sg.assess_sm(testing_inputs, testing_outputs)
print('The surrogate model has been assessed with ' + str(TESTING_SAMPLES) + ' samples!')

# End message
print('Surrogate modeling has finished in '+str(round(time.time()-start_time))+' seconds!')