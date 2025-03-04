import numpy as np
from typing import Protocol, runtime_checkable, Callable, Dict, Any
from functools import partial

# Protocol for objects that have attenuation parameters
@runtime_checkable
class AttenParamsProtocol(Protocol):
    '''Protocol for objects with attenuation parameters'''
    strength: float
    scale: float

# Protocol for objects that can perform attenuation
@runtime_checkable
class AttenuatorProtocol(Protocol):
    '''Protocol for objects that can perform attenuation'''
    def __call__(self, x: np.ndarray, *args, **kwargs) -> np.ndarray: ...

# Function adapter that turns parameter objects and functions into attenuators
def create_attenuator(params: AttenParamsProtocol, func: Callable) -> AttenuatorProtocol:
    """Create an attenuator from parameters and a function."""
    return partial(func, strength=params.strength, scale=params.scale)