import numpy as np
from numpy.lib.stride_tricks import sliding_window_view as swv
from functools import partial
from typing import Callable

def compute_distance(x: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Computes the distance between x and z"""
    return np.linalg.norm(x - z, axis=-1)

def compute_all_distances(x: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Computes the distance for all k x l sensor/source combinations."""
    x = x[None,...] if x.ndim == 2 else x
    z = z[None,...] if z.ndim == 2 else z
    return np.array([compute_distance(x, z) for z in z])

def compute_gradient(x: np.ndarray) -> np.ndarray:
    return partial(np.gradient, axis=-1)(x)

def compute_norm(x: np.ndarray) -> np.ndarray:
    return partial(np.linalg.norm, axis=-1)(x)

def _slicer(arr: np.ndarray, n:int, axis: int) -> np.ndarray:
    slices = [slice(None)] * arr.ndim  # Create a list of "select all" slices
    slices[axis] = slice(None, None, n)  # Modify the slice for the specified axis
    return arr[tuple(slices)]

def naive_path_integral(func: Callable, x: np.ndarray) -> np.ndarray:

    return func(swv(x, window_shape=11, axis=-1)[...,::10,:].mean(axis = -1))