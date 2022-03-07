import numpy as np
import packages.io.plotter as plotter
import packages.error.err_x_area as err_x_area
import packages.error.err_y_area as err_y_area

def main():

    x_data = [[1,2,3,4,5,6,7,8,9,10]]
    exp_y_data = [[x*x for x in x_data[0]]]
    prd_y_data = [[y+1 for y in exp_y_data[0]]]

    plt = plotter.Plotter()
    plt.exp_plot(x_data, exp_y_data)
    plt.prd_plot(x_data, prd_y_data)
    plt.save_plot()

    print('x', err_x_area.ErrXArea(x_data, exp_y_data).get_error(x_data, prd_y_data))
    print('y', err_y_area.ErrYArea(x_data, exp_y_data).get_error(x_data, prd_y_data))
    print('x', err_x_area.ErrXArea(exp_y_data, x_data).get_error(prd_y_data, x_data))   
    print('y', err_y_area.ErrYArea(exp_y_data, x_data).get_error(prd_y_data, x_data))

if __name__ == "__main__":
    main()