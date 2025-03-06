import numpy as np
import scipy.stats as stats

timing_config = {"length": 120, "hz": 10, "trials": 100}
sensor_type_config = {'id': 'toy'}
source_type_config = {'id': 'toy',
                    'strength': 10,
                    'dilution': 'toy',
                    'dilution_params': {'strength': 10, 'scale': 7},
                    'distribution': 'shrink norm'
                    }

sensor_config = {'count': 2, 
                 'type': 'simple',
                 'position_func': 'Linear',
                 'position_args': {'start': np.array([[0,0], [0,50]]),
                                   'velocity': np.array([2 , 1.8]),
                                   'angle': np.array([0,0])}
                 }

source_config = {'count': 1, 
                 'type': 'simple',
                 'position_func': 'Stationary',
                 'position_args': {'start': np.array([[30, 15]])}
                 }

background = {'distr': stats.gengamma, 'params': dict(a=0.75, c = 2.6, loc=0, scale= 0.4625)}

objectives = {'tasks': 'AD', 'models': 'some model objects'}