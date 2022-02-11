"""
 Title: Directory Tracker 
 Description: For tracking the directories created / used
 Author: Janzen Choi

"""

# Libraries
import os

# Constants
DEFAULT_PATH = './'
DEFAULT_FOLDER = 'folder'

# Tracker Class
class Tracker:

    # Constructor
    def __init__(self, path, folder):
        self.path = path
        self.folder = folder
        self.path_folder = path + folder
        self.tracker_num = 1
    
    # Create folder
    def create_directory(self):
        while True:
            try:
                os.mkdir(self.path_folder)
                break
            except:
                self.path_folder = self.path + self.folder + ' (' + str(self.tracker_num) + ')'
                self.tracker_num += 1
    
    # Gets the path and folder
    def get_path_folder(self):
        return self.path_folder + '/'