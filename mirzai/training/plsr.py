# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/api/training/plsr.ipynb.

# %% auto 0
__all__ = ['Learner', 'PLS_model', 'Learners']

# %% ../../nbs/api/training/plsr.ipynb 3
# Python utils
from collections import OrderedDict
from tqdm.auto import tqdm
import glob
from pathlib import Path
import re
import pickle

# mirzai utils
from ..data.loading import load_kssl
from ..data.selection import (select_y, select_tax_order, select_X)
from ..data.transform import (log_transform_y, SNV, TakeDerivative,
                                   DropSpectralRegions, CO2_REGION)
from .metrics import eval_reg
from .core import is_plateau

# Data science stack
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import mean_squared_error

from fastcore.test import *
from fastcore.transform import compose
from fastcore.basics import store_attr

# %% ../../nbs/api/training/plsr.ipynb 5
class Learner():
    def __init__(self, data, model):
        self.X_train, self.X_valid, self.y_train, self.y_valid = data
        self.model = model
        self.n_cpts_best = 1
        
    def find_hp(self, n_cpts_range=range(1,10), delta=0.005, verbose=True):
        perfs = OrderedDict({'n_cpts': [], 'train': [], 'valid': []})
        
        for n_cpts in n_cpts_range:
            self.model.set_params(model__n_components=n_cpts)
            self.model.fit(self.X_train, self.y_train)
            perfs['n_cpts'].append(n_cpts)
            perfs['train'].append(self.model.score(self.X_train, self.y_train))
            perfs['valid'].append(self.model.score(self.X_valid, self.y_valid))
            self.n_cpts_best = n_cpts
            if (is_plateau(-np.array(perfs['valid']), delta=delta, verbose=verbose)):
                return perfs
        return perfs
    
    def fit(self, n_cpts=None):
        if not n_cpts:
            n_cpts = self.n_cpts_best
        self.model.set_params(model__n_components=n_cpts)
        self.model.fit(self.X_train, self.y_train)
        
    def evaluate(self, X, y):
        return self.model.score(X, y)

# %% ../../nbs/api/training/plsr.ipynb 6
class PLS_model():
    "Partial Least Squares model runner"
    def __init__(self, X_names, pipeline_kwargs={}):
        self.X_names = X_names
        self.pipeline_kwargs = pipeline_kwargs
        self.model = None

    def fit(self, data):
        X, y = data
        self.model = Pipeline([
            ('snv', SNV()),
            ('derivative', TakeDerivative(**self.pipeline_kwargs['derivative'])),
            ('dropper', DropSpectralRegions(self.X_names, **self.pipeline_kwargs['dropper'])),
            ('model', PLSRegression(**self.pipeline_kwargs['model']))])
        self.model.fit(X, y)
        return self

    def predict(self, data):
        X, y = data
        return (self.model.predict(X), y)

    def eval(self, data, is_log=True):
        X, y = data
        return eval_reg(y, self.model.predict(X))

# %% ../../nbs/api/training/plsr.ipynb 7
class Learners():
    def __init__(self, 
                 tax_lookup,
                 seeds=range(20), 
                 split_ratio=0.1):
        store_attr() # see https://fastpages.fast.ai/fastcore
         
    def train(self,
              data,
              order=None,
              dest_dir_model='',
              n_cpts_range=range(2, 10),
              delta=1e-2,
              early_stop=1e-4,
              verbose=True):
        
        X, y, tax_order = data                
        for seed in self.seeds:
            print(80*'-')
            print(f'Seed: {seed}')
            print(80*'-')

            #generators = self._get_generators((X, y, tax_order), seed, order=order)
            data_train, data_valid, data_test = self._splitter((X, y, tax_order), seed, order)
            
            model = Pipeline([
                ('snv', SNV()),
                ('derivative', TakeDerivative(window_length=11, polyorder=1, deriv=1)),
                ('dropper', DropSpectralRegions(X_names, regions=CO2_REGION)),
                ('model', PLSRegression())])

            X_train, y_train, _ = data_train
            X_valid, y_valid, _ = data_valid
            learner = Learner((X_train, X_valid, y_train, y_valid), model)

            learner.find_hp(n_cpts_range=n_cpts_range, delta=delta, verbose=False)
            print(f'# of components chosen: {learner.n_cpts_best}')
            learner.fit()
            with open(dest_dir_model/f'model-seed-{seed}.pickle', 'wb') as f: 
                pickle.dump(learner.model, f)
    
    def evaluate(self,
                 data,
                 order=None,
                 src_dir_model=''):
        pass
        X, y, tax_order = data
        perfs = []
        y_hats = []
        y_trues = []
        for fname in glob.glob(str(src_dir_model/'*.pickle')):
            with open(fname, 'rb') as f: 
                model = pickle.load(f)
            seed = int(re.search(r'-(\d+)\.', fname).group(1))
            _, _, data_test = self._splitter((X, y, tax_order), seed, order=order)
            X_test, y_test, _ = data_test
            y_hat = model.predict(X_test)
            perfs.append(eval_reg(y_test, y_hat))
            y_hats.append(y_hat.ravel())
            y_trues.append(y_test.ravel())
        return pd.DataFrame(perfs), pd.DataFrame(y_hats).T, pd.DataFrame(y_trues).T            
    
    def _splitter(self, data, seed, order=None):
        X, y, tax_order = data
        
        # Train/test split
        data = train_test_split(X, 
                                y, 
                                tax_order,
                                test_size=self.split_ratio,
                                random_state=seed) 
        
        X_train, X_test, y_train, y_test, tax_order_train, tax_order_test = data
        data_test = X_test, y_test, tax_order_test
        
        # Further train/valid
        data = train_test_split(X_train, 
                                y_train, 
                                tax_order_train,
                                test_size=self.split_ratio, 
                                random_state=seed)
        X_train, X_valid, y_train, y_valid, tax_order_train, tax_order_valid = data
        data_train = X_train, y_train, tax_order_train
        data_valid = X_valid, y_valid, tax_order_valid
        
        if order is not None:
            data_train, data_valid, data_test = [self._filter(data, order=order) 
                                                 for data in [data_train, data_valid, data_test]]
            
        return data_train, data_valid, data_test
    
    def _filter(self, data, order=None):
        X, y, tax_order = data
        mask = tax_order == order
        return X[mask, :], y[mask], tax_order[mask]