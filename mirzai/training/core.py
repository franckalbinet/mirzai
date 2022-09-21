# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/api/training/core.ipynb.

# %% ../../nbs/api/training/core.ipynb 3
from __future__ import annotations
import numpy as np
import pandas as pd
import pickle
import glob
from pathlib import Path

from fastcore.test import *

# %% auto 0
__all__ = ['is_plateau', 'load_dumps']

# %% ../../nbs/api/training/core.ipynb 4
def is_plateau(array:np.ndarray, # 1D array to test
               w_size:int=3, # Last elements to consider
               delta:float=0.01, # Threshold indicating plateau  
               verbose:bool=True # Display last `w_size` array's elements
              ):
    '''Detect if a plateau is reached when array diffs between last `w_size` below delta'''  
    if len(array) < w_size:
        return False
    pairs_diff = np.convolve(array, [-1, 1], mode='valid')
    is_all_below = np.all(pairs_diff[-w_size:] < delta)
    if verbose:
        print(f'Last pairs diff: {pairs_diff[-w_size:]}')
    return True if is_all_below else False

# %% ../../nbs/api/training/core.ipynb 11
def load_dumps(src_dir):
    """Load all `.pickle` file in specified directory"""
    dumps = []
    for file in glob.glob(str(src_dir/'*.pickle')):
        with open(file, 'rb') as f: 
            dumps.append(pickle.load(f))
    return dumps
