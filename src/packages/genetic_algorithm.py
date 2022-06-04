"""
 Title: Multi-Objective Genetic Algorithm
 Description: For parameter optimisation of the V-P model
 Author: Janzen Choi

"""

# Libraries
import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation, get_termination
from pymoo.optimize import minimize
from pymoo.core.problem import ElementwiseProblem

# Constants
NUM_GENS  = 1000
INIT_POP  = 500
OFFSPRING = 500
CROSSOVER = 0.65
MUTATION  = 0.35

# The Multi-Objective Genetic Algorithm (MOGA) class
class MOGA:
    
    # Constructor
    def __init__(self, model, objective, num_gens = NUM_GENS, init_pop = INIT_POP, offspring = OFFSPRING, crossover = CROSSOVER, mutation = MUTATION):

        # Initialises the members
        self.problem = Problem(model, objective)
        self.num_gens  = num_gens
        self.init_pop  = init_pop
        self.offspring = offspring
        self.crossover = crossover
        self.mutation  = mutation

        # Defines the algorithm and termination condition
        self.algo = NSGA2(
            pop_size     = self.init_pop,
            n_offsprings = self.offspring,
            sampling     = get_sampling("real_lhs"), # real_random
            crossover    = get_crossover("real_sbx", prob=self.crossover, eta=10), # simulated binary
            mutation     = get_mutation("real_pm", prob=self.mutation, eta=15), # polynomial mutation
            eliminate_duplicates = True
        )
        self.term = get_termination("n_gen", self.num_gens)

    # Sets a recorder that records the results during the optimisations
    def set_recorder(self, rec):
        self.problem.rec = rec

    # Runs the genetic optimisation
    def optimise(self):
        params_list = minimize(self.problem, self.algo, self.term, verbose=False, seed=None).X
        return params_list

# The MOGA problem
class Problem(ElementwiseProblem):

    # Constructor
    def __init__(self, model, objective):
        self.objective = objective
        self.model = model
        self.rec = None
        super().__init__(
            n_var    = len(self.model.params),
            n_obj    = len(self.objective.err_collection),
            n_constr = 0,
            xl       = np.array(self.model.l_bnds),
            xu       = np.array(self.model.u_bnds))

    # Minimises expression 'F' such that the expression 'G <= 0' is satisfied
    def _evaluate(self, params, out, *args, **kwargs):
        prd_x_data, prd_y_data = self.model.get_prd_curves(*params)
        err_list = self.objective.get_errors(prd_x_data, prd_y_data)
        if (self.rec != None):
            self.rec.update_results(params, err_list)
        out['F'] = err_list