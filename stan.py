import os
import pystan
import numpy as np
import pandas as pd
import arviz as az
import pickle
from hashlib import md5
import seaborn as sns
import matplotlib.pyplot as plt


# Saving and loading compiled models
def save_stan(obj, filename):
    """Save compiled models for reuse."""
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_stan(filename):
    """Reload compiled models for reuse."""
    return pickle.load(open(filename, 'rb'))


def stan_cache(stan_name, new=False, location=os.path.join('.', 'compiled', '')):
    """Use just as you would stan"""
    file_name = os.path.join('.', 'stan', stan_name)

    # Print out the model code
    with open(file_name, 'r') as stan:
        print(stan.read())

    # Compile model code and save to disk
    code_hash = md5(file_name.encode('ascii')).hexdigest()
    model_name = stan_name.split('.')[0]
    if '/' in model_name:
        model_name = model_name.split('/')[-1]
    elif '\\' in model_name:
        model_name = model_name.split('\\')[-1]
    cache_fn = location + f'{model_name}-cached-{code_hash}.pkl'

    if new:
        sm = pystan.StanModel(file=file_name, model_name=model_name)
        with open(cache_fn, 'wb') as f:
            pickle.dump(sm, f)
    else:
        try:
            sm = pickle.load(open(cache_fn, 'rb'))
        except:
            sm = pystan.StanModel(file=file_name, model_name=model_name)
            with open(cache_fn, 'wb') as f:
                pickle.dump(sm, f)
        else:
            print("Using cached StanModel")

    return sm
