"""
 Title: Multi-Objective Genetic Algorithm
 Description: For parameter optimisation of the V-P model
 Author: Janzen Choi

"""

# Libraries
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation, get_termination
from pymoo.optimize import minimize

# Constants
NUM_GENS  = 1
INIT_POP  = 5
OFFSPRING = 5
CROSSOVER = 0.65 # 0.65
MUTATION  = 0.35 # 0.35

# The Multi-Objective Genetic Algorithm (MOGA) class
class MOGA:
    
    # Constructor
    def __init__(self, objective):

        # Initialises the members
        self.objective = objective
        self.num_gens  = NUM_GENS
        self.init_pop  = INIT_POP
        self.offspring = OFFSPRING
        self.crossover = CROSSOVER
        self.mutation  = MUTATION

        # Defines the algorithm and termination condition
        self.algo = NSGA2(
            pop_size     = self.init_pop,
            n_offsprings = self.offspring,
            sampling     = get_sampling("real_random"),
            crossover    = get_crossover("real_sbx", prob=self.crossover, eta=10), # simulated binary
            mutation     = get_mutation("real_pm", prob=self.mutation, eta=15), # polynomial mutation
            eliminate_duplicates = True)
        self.term = get_termination("n_gen", self.num_gens)

    # Runs the genetic optimisation
    def optimise(self):
        params_list = minimize(self.objective, self.algo, self.term, verbose=True, seed=None).X
        return params_list