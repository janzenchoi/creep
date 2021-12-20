"""
 Title: Excel I/O
 Description: For reading and writing to .xlsx files
 Author: Janzen Choi

"""

# Libraries
import os
import pandas as pd

# Constants
DEFAULT_PATH    = './'
DEFAULT_FILE    = 'excel'
DEFAULT_SHEET   = 'info'

# Class for reading and writing to .xlsx files
class Excel:

    # Constructor
    def __init__(self, path = DEFAULT_PATH, file = DEFAULT_FILE, sheet = DEFAULT_SHEET):
        self.path   = path
        self.file   = file
        self.sheet  = sheet

    # Sets the default values if empty
    def set_default(self, path, file, sheet):
        path = self.path if path == '' else path        
        file = self.file if file == '' else file
        sheet = self.sheet if sheet == '' else sheet
        return path, file, sheet

    # Reads a column of data and returns it in the form of a list
    def read_column(self, column, path = '', file = '', sheet = ''):
        path, file, sheet = self.set_default(path, file, sheet)
        data = pd.read_excel(io = path + file + '.xlsx', sheet_name = sheet, usecols = [column])
        data = data.dropna()
        data = data.values.tolist()
        data = [d[0] for d in data]
        return data

    # Gets a list of data only for the included tests
    def read_included(self, column):
        info_list = self.read_column(column = column, sheet = 'info')
        include_list = self.read_column(column = 'include', sheet = 'info')
        info_list = [info_list[i] for i in range(0,len(include_list)) if int(include_list[i]) == 1]
        return info_list

    # Writes to an excel (appends a number if the filename already exists)
    def write_data(self, data, columns, path = '', file = '', sheet = '', max_files = 100):
        path, file, sheet = self.set_default(path, file, sheet)
        df = pd.DataFrame(data, columns = columns)
        target_file = path + file + '.xlsx'        
        for file_num in range(1, max_files):
            try:
                if os.path.isfile(target_file):
                    target_file = path + file + ' (' + str(file_num) + ').xlsx'
                df.to_excel(target_file, sheet_name = sheet)
                break
            except:
                continue
    
    # Appends to an existing excel
    def append_data(self, data, columns, path = '', file = '', sheet = ''):
        path, file, sheet = self.set_default(path, file, sheet)

        # Read old data
        if os.path.isfile(path + file + '.xlsx'):
            old_data = [self.read_column(column, path, file, sheet) for column in columns]
            old_data = [[column[i] for column in old_data] for i in range(len(old_data[0]))]
            data = old_data + data

        # Append new data to old data and write
        df = pd.DataFrame(data, columns = columns)
        df.to_excel(path + file + '.xlsx', sheet_name = sheet)