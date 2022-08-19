from .result import Result
from .algorithm_instance import AlgorithmInstance
from .save_handler import SaveHandler
from .config import RS_ITER_NUM, SAVE_PATH
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn


class Algorithm:
    def __init__(self, name, func, param_space, version=1):
        self.name = name
        self.func = func
        self.param_space = param_space
        self.version = version
        self.best_instance = None

        self.save_handler = SaveHandler(
            os.path.join(SAVE_PATH, f'{self.name}-{self.version}')
        )

        self.instances = set()

        self.load_instances()

    def __call__(self, **params) -> Result:
        return self.func(**params)
    
    def generate_random_instance(self):
        params = {}
        for param, values in self.param_space.items():
            params[param] = np.random.choice(values)
        return AlgorithmInstance(self, params, self.save_handler)
    
    def load_instances(self):
        instances = self.save_handler.get_all_instances()
        self.instances.update(instances)
    
    def tune_params(
        self,
        method='random',
        iter_num=RS_ITER_NUM,
        metric='hv',
        mode='max',
    ):
        if method == 'random':

            instances = list(self.instances)

            while len(instances) < iter_num:
                new_instance = self.generate_random_instance()
                instances.append(new_instance)

            best_value = float('-inf') if mode == 'max' else float('inf')

            for i, current_instance in enumerate(instances[:iter_num], 1):
                print(f'Calculating instance {i} / {iter_num}')
                current_value = current_instance.success_metrics()[metric]
                print(f'{metric} = {current_value}')
                if (mode == 'max' and current_value >= best_value)\
                    or (mode == 'min' and current_value <= best_value):
                    best_value = current_value
                    self.best_instance = current_instance
                
                print()
            
            self.instances.update(instances)
            
        else:
            raise NotImplementedError 
    

    def plot_instances(self, x_metric='avg_success_eval', y_metric='failure_rate'):
        instances = list(self.instances)
        xs = []
        ys = []

        for instance in instances:
            metrics = instance.success_metrics()
            xs.append(metrics[x_metric])
            ys.append(metrics[y_metric])
        
        plt.scatter(xs, ys)
        plt.xlabel(x_metric)
        plt.ylabel(y_metric)
        plt.title(f'Performance metrics of {self.name} across {len(instances)} instances')
        plt.show()
    
    def plot_all(self):
        instances = list(self.instances)
        df = pd.DataFrame([instance.success_metrics() for instance in instances])
        df.drop(['failure_rate', 'success_cnt'], axis=1, inplace=True)
        seaborn.pairplot(df)
        plt.show()