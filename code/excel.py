"""
 Title: Excel I/O functions
 Description: For reading and writing to .xlsx files
 Author: Janzen Choi

"""

# Libraries
import os
import pandas as pd

# Constants
DATA_FILE = '../alloy_617'
INFO_SHEET = 'info'
STRAIN_SHEET = 'data'
PARAMS_FILE  = '../results/params'

# Reads a column of data and returns it in the form of a list
def read_column(column_name, sheet_name = INFO_SHEET, file_name = DATA_FILE):
    data = pd.read_excel(io=file_name+'.xlsx', sheet_name=sheet_name, usecols=[column_name])
    data = data.dropna()
    data = data.values.tolist()
    data = [d[0] for d in data]
    return data

# Gets a list of data only for the included tests
def read_included(column_name):
    info_list = read_column(column_name, INFO_SHEET, DATA_FILE)
    include_list = read_column('include', INFO_SHEET, DATA_FILE)
    info_list = [info_list[i] for i in range(0,len(include_list)) if int(include_list[i]) == 1]
    return info_list

# Writes to an excel (appends a number if the filename already exists)
def write_columns(data, column_names, sheet_name = 'params', file_name = PARAMS_FILE, max_files = 100):
    df = pd.DataFrame(data, columnn = column_names)
    target_file = file_name + '.xlsx'
    for file_num in range(1, max_files):
        try:
            if os.path.isfile(target_file):
                target_file = file_name + ' (' + str(file_num) + ').xlsx'
            df.to_excel(target_file, sheet_name = sheet_name)
            break
        except:
            continue