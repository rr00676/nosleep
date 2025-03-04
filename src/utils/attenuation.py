import numpy as np
from typing import Callable, Protocol, runtime_checkable

def inv_sql(x:np.ndarray, strength:float = 1.0, scale:float = 1.0, tol:float = 1e-3) -> np.ndarray:
    """Simple inverse square law function."""
    d = np.where(x/scale < tol, tol, x/scale)
    return strength/d**2

def exponential(x:np.ndarray, strength:float = 1.0, scale:float = 1.0) -> np.ndarray:
    """Simple exponential decay function."""
    return strength*np.exp(-x/scale)