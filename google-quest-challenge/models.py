from utils import root_path
import pandas as pd
import numpy as np
import scipy as scp


class RandomModel:
    def __init__(self):
        self.model = None

    def train(self, X, y):
        self.model = 1

    def predict(self, X):
        assert self.model is not None
        return np.random.random(len(X), 30)

    def save(self, path):
        # TODO Implement
        pass

    def load(self, path):
        # TODO Implemnett
        pass
