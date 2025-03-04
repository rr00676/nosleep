import numpy as np
from typing import Protocol, runtime_checkable, TypeVar, Optional, Tuple, Any, Dict, Callable

T = TypeVar('T', bound=np.ndarray)

@runtime_checkable
class DistributionProtocol(Protocol):
    """Objects that represent probability distributions"""
    dist: Any
    params: Dict[str, Any]
    
    def sample(self, size: Optional[Tuple[int, ...]] = None) -> np.ndarray: ...
    def eval_params(self, distances: np.ndarray, attenuator: Callable[[np.ndarray], np.ndarray]) -> Dict[str, Any]: ...