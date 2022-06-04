"""
 Title: Main file
 Description: Main file for creep prediction
 Author: Janzen Choi

"""

# Libraries
import time, json, os, threading
import packages.optimiser as optimiser

# IO Constants
DATA_PATH           = './'
DATA_FILE           = 'alloy_617'
RECORD_PATH         = './results/'
INPUT_FILE          = 'input.txt'
HISTORY_FILE        = 'history.txt'

# Optimisation constants
CHECK_INTERVAL      = 10
NUM_THREADS         = 1 + 5

# Available Setting
AVAILABLE_MODELS    = ['visco_plastic']
AVAILABLE_TESTS     = ['G32', 'G33', 'G44', 'G25']
AVAILABLE_ERRORS    = ['err_dy_min', 'err_dy_area', 'err_x_area', 'err_y_area', 'err_x_end', 'err_y_end']

# Default Settings
DEFAULT_MODEL       = 'visco_plastic'
DEFAULT_TESTS       = ['G44', 'G25']
DEFAULT_ERRORS      = ['err_dy_area', 'err_x_area', 'err_x_end', 'err_y_end']
DEFAULT_NUM_GENS    = 100
DEFAULT_INIT_POP    = 300
DEFAULT_OFFSPRING   = 399
DEFAULT_CROSSOVER   = 0.65
DEFAULT_MUTATION    = 0.35
# {"model": "visco_plastic", "tests": ["G44", "G25"], "errors": ["err_dy_area", "err_x_area", "err_x_end", "err_y_end"], "moga": {"num_gens": 10, "init_pop": 10, "offspring": 10, "crossover": 0.65, "mutation": 0.35}}

# Main function
def main():

    # Initialisation
    open(RECORD_PATH + HISTORY_FILE, 'w').close() # create / truncate history file
    optimisation_queue = get_settings_list()
    history_list = []

    # Continually runs optimisations
    identifier = 0
    while True:

        # Check if a thread is available
        if threading.active_count() < NUM_THREADS and len(optimisation_queue) > 0:

            # Pops settings of next optimisation
            settings = optimisation_queue.pop(0)

            # Conduct optimisation if settings are valid
            if (is_sublist([settings['model']], AVAILABLE_MODELS)
            and is_sublist(settings['tests'], AVAILABLE_TESTS)
            and is_sublist(settings['errors'], AVAILABLE_ERRORS)):

                # Write settings in history
                try:
                    history_list.append(str(settings))
                    history_file = open(RECORD_PATH + HISTORY_FILE, 'w')
                    history_file.write('\n'.join(history_list))
                    history_file.close()
                except:
                    pass

                # Conduct optimisation
                opt = optimiser.Optimiser(settings, identifier, DATA_PATH, DATA_FILE, RECORD_PATH)
                opt.start()
            else:
                print('[' + str(identifier).zfill(3) + ']: Optimisation settings are incorrect (skipping)')
            identifier += 1
        
        # Wait until conducting another optimisation
        time.sleep(CHECK_INTERVAL)
        optimisation_queue += get_settings_list()

# Reads all the text files and returns them
def get_settings_list():
    settings_list = []
    if INPUT_FILE in os.listdir(RECORD_PATH):
        read_file = open(RECORD_PATH + INPUT_FILE, 'r')
        while (settings := read_file.readline().rstrip()):
            settings_list.append(settings)
        read_file.close()
        os.remove(RECORD_PATH + INPUT_FILE)
        return [json.loads(settings) for settings in settings_list]
    else:
        return []

# Fill the empty values of the settings with default values
def fill_voids(settings):
    if not settings.__contains__('model'):
        settings.update({'model': DEFAULT_MODEL})
    if not settings.__contains__('tests'):
        settings.update({'tests': DEFAULT_TESTS})
    if not settings.__contains__('errors'):
        settings.update({'errors': DEFAULT_ERRORS})
    if not settings.__contains__('moga'):
        settings.update({
            'moga': {
                'num_gens': DEFAULT_NUM_GENS,
                'init_pop': DEFAULT_INIT_POP,
                'offspring': DEFAULT_OFFSPRING,
                'crossover': DEFAULT_CROSSOVER,
                'mutation': DEFAULT_MUTATION
            }
        })
    else:
        if not settings['moga'].__contains__('num_gens'):
            settings['moga'].update({'num_gens': DEFAULT_NUM_GENS})
        if not settings['moga'].__contains__('init_pop'):
            settings['moga'].update({'init_pop': DEFAULT_INIT_POP})
        if not settings['moga'].__contains__('offspring'):
            settings['moga'].update({'offspring': DEFAULT_OFFSPRING})
        if not settings['moga'].__contains__('crossover'):
            settings['moga'].update({'crossover': DEFAULT_CROSSOVER})
        if not settings['moga'].__contains__('mutation'):
            settings['moga'].update({'mutation': DEFAULT_MUTATION})
    return settings

# Check if sublist (order ignored)
def is_sublist(sublist, list):
    for item in sublist:
        if item not in list:
            return False
    return True

# Main function caller
if __name__ == '__main__':
    main()