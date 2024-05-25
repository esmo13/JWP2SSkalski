import game
import numpy as np
import random


class AugmentedRandomSearchAgent():
    def __init__(self, num_of_directions, step_size, std_dev_of_noise, considered_best_directions):
        self.N = num_of_directions
        self.alpha = step_size
        self.v = std_dev_of_noise
        self.b = considered_best_directions
        
        pass
