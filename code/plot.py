"""
 Title: Plotting functions
 Description: For plotting data
 Author: Janzen Choi

"""

# Libraries
import matplotlib.pyplot as plt

# Constants
PLOT_NAME = '../results/plot'
EXP_DATA_COLOUR = 'darkgrey'
PRD_DATA_COLOUR = 'r'

# Prepares the plot
def prep_plot(title = '', xlabel = 'x', ylabel = 'y'):
    plt.figure(figsize=(8,8))
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.title(title, fontsize=20)
    
# Plots the experimental data using a scatter plot
def exp_plot(exp_x_data, exp_y_data):
    for i in range(0, len(exp_x_data)):
        plt.scatter(exp_x_data[i], exp_y_data[i], marker='o', color=EXP_DATA_COLOUR, linewidth=1)
    
# Plots the predicted data using a line plot
def prd_plot(prd_x_data, prd_y_data):
    for i in range(0, len(prd_x_data)):
        plt.plot(prd_x_data[i], prd_y_data[i], PRD_DATA_COLOUR)

# Saves the plot
def save_plot(fig_name = PLOT_NAME):
    plt.savefig(fig_name)