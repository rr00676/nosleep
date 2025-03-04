# base/factories.py
from typing import Dict, List, Callable, Any, Optional
import numpy as np
from base.experiment import Experiment
from base.field import FieldObjectProtocol, SourceProtocol, SensorProtocol, Source, Sensor # Import concrete classes
from base.attenuation import AttenuatorProtocol, create_attenuator, AttenParamsProtocol # Assuming create_attenuator is in base/attenuation.py
from base.distribution import DistributionProtocol # Assuming DistributionProtocol is in base/distribution.py - adjust if needed
from utils.motion import linear, stationary, elliptical # Import motion functions from utils
from utils.attenuation import inv_sql, exponential # Import attenuation functions from utils
from utils.functional import f_kwargs
from scipy import stats # Import scipy.stats for distributions
from base.experiment_setup import ExperimentSetup # Import ExperimentSetup dataclass
from base.pathing import PathArr # Import PathArr dataclass


def create_experiment(exp_dict: Dict) -> Experiment:
    """Creates an Experiment object from a dictionary, raising errors if definition is incorrect."""
    required_keys = ['time', 'hz', 'trials']
    for key in required_keys:
        if key not in exp_dict:
            raise ValueError(f"Experiment definition is incorrect: missing key '{key}'. Required keys are: {required_keys}")
    duration = exp_dict['time']
    hz = exp_dict['hz']
    trials = exp_dict['trials']
    return Experiment(duration=duration, hz=hz, trials=trials)


# Function to resolve function names (strings) to actual functions
def resolve_function(func_name: str) -> Callable:
    """Resolves a function name string to a function object."""
    function_map = { # Expand this map as needed
        'linear': linear,
        'elliptical': elliptical, # Placeholder for elliptical
        'stationary': stationary,
        'inv_sql': inv_sql,
        'exponential': exponential,
        'norm': stats.norm # For scipy.stats.norm (normal distribution)
    }
    func = function_map.get(func_name)
    if not func:
        raise ValueError(f"Unknown function name: {func_name}")
    return func


def create_paths(exp: Experiment, obj_dicts: List[Dict]) -> PathArr:
    """Generates motion paths for all field objects and returns a PathArr."""
    source_paths_list: List[np.ndarray] = []
    sensor_paths_list: List[np.ndarray] = []

    for obj_dict in obj_dicts:
        name = obj_dict.get('name', 'unnamed_object') # Default name if not provided
        count = obj_dict.get('count', 1)
        motion_func_name = obj_dict.get('motion')
        motion_params_dict = obj_dict.get('motion_params', {})
        motion_function = resolve_function(motion_func_name) if motion_func_name else stationary # Default to stationary

        paths_list: List[np.ndarray] = []
        for _ in range(count):
            combined_params = {**motion_params_dict, 'steps': exp.steps, 'dt': exp.dt}
            path = f_kwargs(motion_function, combined_params) # Pass dt here!
            paths_list.append(path)

        if 'atten' in obj_dict or 'dist' in obj_dict: # Heuristic to identify sources
            source_paths_list.extend(paths_list)
        else: # Assume sensors otherwise
            sensor_paths_list.extend(paths_list)

    return PathArr(source_paths=source_paths_list, sensor_paths=sensor_paths_list)


def create_source(attenuator: Optional[AttenuatorProtocol] = None, distribution: Optional[DistributionProtocol] = None) -> Source:
    """Creates a single Source object."""
    return Source(attenuator=attenuator, distribution=distribution)


def create_sensor() -> Sensor:
    """Creates a single Sensor object."""
    return Sensor()


def create_experiment_setup(exp_dict: Dict, obj_dicts: List[Dict]) -> ExperimentSetup:
    """Orchestrates the creation of an experiment setup from dictionaries."""
    experiment = create_experiment(exp_dict)
    path_arr = create_paths(experiment, obj_dicts) # Get PathArr object
    sources: List[Source] = []
    sensors: List[Sensor] = []

    # Path assignment logic removed from here - paths are in path_arr, not attached to objects

    for obj_dict in obj_dicts:
        name = obj_dict.get('name', 'unnamed_object')
        count = obj_dict.get('count', 1)

        # --- Handle Attenuation and Distribution (for Sources) ---
        atten_func_name = obj_dict.get('atten')
        atten_params_dict = obj_dict.get('atten_params', {})
        atten_function = resolve_function(atten_func_name) if atten_func_name else None

        dist_func_name = obj_dict.get('dist')
        dist_params_dict = obj_dict.get('dist_params', {}) # Not used yet
        distribution_function = resolve_function(dist_func_name) if dist_func_name else None

        for _ in range(count): # No path assignment here anymore
            attenuator = None
            distribution = None

            if atten_function:
                class DictAttenParams: # Simple class to mimic AttenParamsProtocol from a dict
                    def __init__(self, params):
                        for k, v in params.items():
                            setattr(self, k, v)
                atten_params = DictAttenParams(atten_params_dict) # Create parameter object from dict
                attenuator = create_attenuator(atten_params, atten_function)

            if distribution_function:
                distribution = distribution_function # Placeholder

            if attenuator or distribution_function: # Heuristic for Source
                source = create_source(attenuator=attenuator, distribution=distribution) # No path argument
                sources.append(source)
            else: # Assume Sensor
                sensor = create_sensor() # No path argument
                sensors.append(sensor)


    return ExperimentSetup( # Create and return ExperimentSetup object
        experiment=experiment,
        sources=sources,
        sensors=sensors,
        paths=path_arr # PathArr object is still returned
    )