"""
 Title: An ANN for surrogate modeling
 Description: For creating the ANN surrogate model for the V-P model
 Author: Janzen Choi

"""

# General Libraries
import time
import tensorflow as tf
import keras
from keras import layers
from keras.regularizers import l2, l1_l2

# Custom Libraries
import packages.sampler as sampler
import packages.polyfier as polyfier
import packages.model.visco_plastic as visco_plastic
import packages.mapper as mapper
import packages.io.excel as excel
import packages.io.plotter as plotter
import packages.polyfier as polyfier

# Constants
DATA_PATH   = './'
DATA_FILE   = 'alloy_617'
RESULT_PATH = './results/'
RESULT_FILE = 'rnn_plot'
MODEL_PATH  = './results/'
MODEL_FILE  = 'model'
PARAMS_LIST = visco_plastic.PARAMS
POLY_DEG    = polyfier.DEFAULT_POLY_DEG

# Bound Constants (for linear mapping)
PARAMS_LOWER = visco_plastic.L_BNDS
PARAMS_UPPER = visco_plastic.U_BNDS
STRAIN_LOWER = 0
STRAIN_UPPER = 100

# ANN Constants
LEARNING_RATE   = 0.01
NUM_EPOCHS      = 10
BATCH_SIZE      = 20
TRAIN_SIZE      = 5000
TEST_SIZE       = 1000
ACTIVATION      = 'relu'

# Main function
def main():

    # Initialisation
    start_time = time.time()
    print('=================================================================')
    print('ANN modelling has begun!')

    # Prepare testing and training samples
    sp = sampler.Sampler()
    training_outputs, training_inputs = sp.sample(TRAIN_SIZE)
    testing_outputs, testing_inputs = sp.sample(TEST_SIZE)
    print('Samples read in!')

    # Map the inputs
    strain_mapper = mapper.StrainMapper(STRAIN_LOWER, STRAIN_UPPER)
    training_inputs = strain_mapper.map(training_inputs)
    testing_inputs = strain_mapper.map(testing_inputs)
    print('Inputs processed')

    # Map the outputs
    params_mapper = mapper.ParameterMapper(PARAMS_LOWER, PARAMS_UPPER)
    training_outputs = params_mapper.map(training_outputs)
    testing_outputs = params_mapper.map(testing_outputs)
    print('Outputs processed')

    # Construct the model
    model = get_model(training_inputs, training_outputs)
    print('=================================================================')
    model.summary()
    print('=================================================================')
    print('Model has been created!')

    # Conduct the optimisation
    xy_fit = model.fit(training_inputs, training_outputs, epochs = NUM_EPOCHS, batch_size = BATCH_SIZE, validation_data = (testing_inputs, testing_outputs), verbose=2)
    print('ANN modelling has concluded!')
    print('=================================================================')
    print('Training Loss:', xy_fit.history['loss'][-1] * 100, '%')
    print('Validation Loss:', xy_fit.history['val_loss'][-1] * 100, '%')
    print('Training Accuracy:', xy_fit.history['accuracy'][-1] * 100, '%')
    print('Validation Accuracy:', xy_fit.history['val_accuracy'][-1] * 100, '%')
    print('=================================================================')

    # Gets the experimental data
    exp_x_data, exp_y_data, exp_stresses = get_exp_data()
    print('The experimental data for ' + str(len(exp_x_data)) + ' test(s) has been read!')

    # Predict the parameters
    prd_x_data, prd_y_data = get_prd_data(exp_x_data, exp_y_data, exp_stresses, strain_mapper, params_mapper, model)
    print('The predicted curves have been retrieved!')
    
    # Plot the results
    plot_results(exp_x_data, exp_y_data, prd_x_data, prd_y_data)
    print('The experimental and predicted curves have been plotted!')

    # End message
    print('Program finished at ' + time.strftime('%H:%M:%S', time.localtime()) + ' in ' + str(round(time.time()-start_time)) + ' seconds!')
    print('=================================================================')

# Gets the experimental data
def get_exp_data():
    xl = excel.Excel(path = DATA_PATH, file = DATA_FILE)
    test_names = xl.read_included('test')
    exp_x_data = [xl.read_column(column = test_name + '_time', sheet = 'data') for test_name in test_names]
    exp_y_data = [xl.read_column(column = test_name + '_strain', sheet = 'data') for test_name in test_names]
    exp_stresses = xl.read_included('stress')
    return exp_x_data, exp_y_data, exp_stresses

# Gets the predicted data
def get_prd_data(exp_x_data, exp_y_data, exp_stresses, strain_mapper, params_mapper, model):
    vp = visco_plastic.ViscoPlastic(exp_stresses)
    pf = polyfier.Polyfier()
    _, tst_y_data = pf.curves_to_curves(exp_x_data, exp_y_data)
    mapped_tst_y_data = strain_mapper.unmap(tst_y_data)
    mapped_params = model.predict(mapped_tst_y_data)
    params = params_mapper.unmap(mapped_params)[0]
    prd_x_data, prd_y_data = vp.get_prd_curves(*params)
    return prd_x_data, prd_y_data

# Creates the model
def get_model(training_inputs, training_outputs):

    # Define the model's structure
    model = keras.Sequential()
    model.add(layers.Embedding(input_dim = len(training_inputs[0]), output_dim = 256))
    model.add(layers.GRU(units = 128, return_sequences = True))
    # model.add(layers.SimpleRNN(units = 64))
    # model.add(layers.Dropout(0.25))
    
    # Dense hidden layer (with regulariser)
    model.add(layers.Dense(units = 32, kernel_regularizer = l1_l2(l1 = 1e-5, l2 = 1e-4), bias_regularizer = l2(1e-4), activity_regularizer = l2(1e-5), activation = 'relu'))
    
    # Output layer
    model.add(layers.Dense(units = len(training_outputs[0]), activation = 'sigmoid'))

    # Build and compile the model
    model.build((None, None, len(training_inputs[0])))
    model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = [keras.metrics.RootMeanSquaredError(), 'mean_absolute_percentage_error'])

    # Save and return the model
    # model.save_weights(MODEL_PATH + MODEL_FILE)
    return model

# Plots rhe results
def plot_results(exp_x_data, exp_y_data, prd_x_data, prd_y_data):
    pt = plotter.Plotter(path = RESULT_PATH, plot = RESULT_FILE)
    pt.prep_plot()
    pt.exp_plot(exp_x_data, exp_y_data)
    pt.prd_plot(prd_x_data, prd_y_data)
    pt.save_plot()

# Calls the main function
if __name__ == '__main__':
    main()