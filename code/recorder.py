"""
 Title: Recorder
 Description: Specifically for recording data as the MOGA operates
 Author: Janzen Choi

"""

# Libraries
import plot
import numpy

# Constants
RECORD_INTERVAL = 10
POPULATION_LIMIT = 100

# The Recorder class
class Recorder:

    # Constructor
    def __init__(self, init_pop, offspring):
        self.init_pop = init_pop
        self.offspring = offspring
        self.num_evals = 0
        self.opt_params = []
        self.opt_errors = []

    # Maintains a sorted list of the top X optimal parameters 
    def update_population(self, params, err_list):
        err_total = numpy.average(err_list)
        
        # If the stored parameters exceed the limit, remove the worst
        if len(self.opt_params) == POPULATION_LIMIT:
            if self.opt_errors[-1][-1] < err_total:
                return
            self.opt_params.pop()
            self.opt_errors.pop()

        # Adds new params in order
        inserted = False
        for i in range(0, len(self.opt_params)):
            if err_total < self.opt_errors[i][-1]:
                self.opt_params.insert(i, params)
                self.opt_errors.insert(i, err_list + [err_total])
                inserted = True
                break

        # If new params is worst between existing params
        if not inserted:
            self.opt_params.append(params)
            self.opt_errors.append(err_list + [err_total])

    # Determines whether to record
    def should_record(self):
        return (self.num_evals - self.init_pop) % self.offspring != 0
    
    