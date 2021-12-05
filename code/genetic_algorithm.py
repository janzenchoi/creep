"""
 Title: Multi-Objective Genetic Algorithm
 Description: For parameter optimisation of the V-P model
 Author: Janzen Choi

"""

# Libraries
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation, get_termination
from pymoo.optimize import minimize

# Constants
NUM_GENS  = 100
INIT_POP  = 10
OFFSPRING = 10
CROSSOVER = 0.65
MUTATION  = 0.35

# The Multi-Objective Genetic Algorithm (MOGA) class
class MOGA:
    
    # Constructor
    def __init__(self, objective):
        self.objective = objective
        self.algo = NSGA2(
            pop_size     = INIT_POP,
            n_offsprings = OFFSPRING,
            sampling     = get_sampling("real_random"),
            crossover    = get_crossover("real_sbx", prob=CROSSOVER, eta=10), # simulated binary
            mutation     = get_mutation("real_pm", prob=MUTATION, eta=15), # polynomial mutation
            eliminate_duplicates = True)
        self.term = get_termination("n_gen", NUM_GENS)

    # Runs the genetic optimisation
    def optimise(self):
        params_list = minimize(self.objective, self.algo, self.term, verbose=True, seed=None).X
        return params_list