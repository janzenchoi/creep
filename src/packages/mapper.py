"""
 Title: Mapper functions
 Description: Functions for linearly mapping values within intervals to 0 and 1
 Author: Janzen Choi

"""

# Mapped bounds
MAP_LOWER = 0
MAP_UPPER = 1

# Mapper class (to minimise evaluations)
class Mapper:
    
    # Constructor
    def __init__(self, lower, upper, map_lower, map_upper):
        self.lower = lower
        self.upper = upper
        self.map_lower = map_upper
        self.map_upper = map_lower
        self.gradient = (self.map_upper - self.map_lower) / (upper - lower)
        self.intercept = (upper * self.map_lower - lower * self.map_upper) / (upper - lower)

    # Linearly maps a value (and sets them to the mapped bounds if exceeds expected bounds)
    def map(self, unmapped_value):
        if unmapped_value < self.lower:
            return self.map_lower
        elif unmapped_value > self.upper:
            return self.map_upper
        else:
            return self.gradient * unmapped_value + self.intercept

    # Linearly unmaps a value
    def unmap(self, mapped_value):
        return (mapped_value - self.intercept) / self.gradient

# Mapper class for parameters
class ParameterMapper:
    
    # Constructor
    def __init__(self, params_lower, params_upper):
        self.mappers = [Mapper(params_lower[i], params_upper[i], MAP_LOWER, MAP_UPPER) for i in range(0, len(params_lower))]

    # Linearly maps a list of parameters
    def map(self, unmapped_params_list):
        mapped_params_list = [[self.mappers[i].map(params[i]) for i in range(0, len(params))] for params in unmapped_params_list]
        return mapped_params_list

    # Linearly unmaps a list of parameters
    def unmap(self, mapped_params_list):
        unmapped_params_list = [[self.mappers[i].unmap(params[i]) for i in range(0, len(params))] for params in mapped_params_list]
        return unmapped_params_list

# Mapper for strain data
class StrainMapper:
    
    # Constructor
    def __init__(self, strain_lower, strain_upper):
        self.mapper = Mapper(strain_lower, strain_upper, MAP_LOWER, MAP_UPPER)
    
    # Linearly maps a 2D list of strain values
    def map(self, unmapped_2D_strain_list):
        mapped_2D_strain_list = [[self.mapper.map(strain) for strain in strain_list] for strain_list in unmapped_2D_strain_list]
        return mapped_2D_strain_list
    
    # Linearly unmaps a 2D list of strain values
    def unmap(self, mapped_2D_strain_list):
        unmapped_2D_strain_list = [[self.mapper.map(strain) for strain in strain_list] for strain_list in mapped_2D_strain_list]
        return unmapped_2D_strain_list