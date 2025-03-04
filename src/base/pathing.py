import numpy as np
from typing import Protocol, runtime_checkable, TypeVar, Any, Dict, Callable, Type, List
import inspect
from dataclasses import dataclass

@dataclass
class PathArr:
    """Dataclass to hold path arrays for sources and sensors."""
    source_paths: List[np.ndarray]
    sensor_paths: List[np.ndarray]
T = TypeVar('T', bound=np.ndarray)

@runtime_checkable
class PathGeneratorProtocol(Protocol):
    """Protocol for objects that generate motion paths"""
    def __call__(self, steps: int, **kwargs) -> np.ndarray: ...

import numpy as np

@dataclass
class PathArr:
    """Dataclass to hold path arrays for sources and sensors."""
    source_paths: List[np.ndarray]
    sensor_paths: List[np.ndarray]