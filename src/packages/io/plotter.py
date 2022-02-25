"""
 Title: Plotter
 Description: For plotting data
 Author: Janzen Choi

"""

# Libraries
import matplotlib.pyplot as plt

# Constants
DEFAULT_PATH    = './'
DEFAULT_PLOT    = 'plot'
EXP_DATA_COLOUR = 'darkgrey'
PRD_DATA_COLOUR = 'r'

# Class for plotting
class Plotter:

    # Constructor
    def __init__(self, path = DEFAULT_PATH, plot = DEFAULT_PLOT):
        self.path = path
        self.plot = plot

    # Prepares the plot
    def prep_plot(self, title = '', xlabel = 'x', ylabel = 'y'):
        plt.figure(figsize=(8,8))
        plt.xlabel(xlabel, fontsize=20)
        plt.ylabel(ylabel, fontsize=20)
        plt.title(title, fontsize=20)
        
    # Plots the experimental data using a scatter plot
    def exp_plot(self, exp_x_data, exp_y_data, colour = EXP_DATA_COLOUR):
        for i in range(0, len(exp_x_data)):
            plt.scatter(exp_x_data[i], exp_y_data[i], marker='o', color=colour, linewidth=1)
        
    # Plots the predicted data using a line plot
    def prd_plot(self, prd_x_data, prd_y_data, colour = PRD_DATA_COLOUR):
        for i in range(0, len(prd_x_data)):
            plt.plot(prd_x_data[i], prd_y_data[i], colour)

    # Saves the plot
    def save_plot(self, path = '', plot = ''):
        path = self.path if path == '' else path
        plot = self.plot if plot == '' else plot
        plt.savefig(path + plot)