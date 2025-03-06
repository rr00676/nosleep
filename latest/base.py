import numpy as np
from numpy.typing import NDArray
from utils.functional import f_kwargs
from utils.math import compute_all_distances
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol, Callable, runtime_checkable, Tuple
from functools import partial

@runtime_checkable
class Identifiable(Protocol):
    """Protocol for objects that can be identified by an ID."""
    @property
    def id(self) -> str: ...

@dataclass
class RV:
    id: str
    func: Callable = field(default_factory = lambda x: x)
    params: Dict[str, Any] = field(default_factory=dict)
    
@dataclass
class StatsRV(RV):
    def mean(self):
        return self.func(**self.params).mean()
    
    def sample(self, n:int|Tuple[int]):
        return self.func(**self.params).rvs(size=n)

@dataclass
class Dilution:
    id: str = None
    func: Callable = field(default_factory = lambda x: x)
    params: Dict[str, Any] = field(default_factory=dict)
    curried: Callable = field(init=False)

    def __post_init__(self):
        self.curried = partial(self.func, **self.params)


@dataclass
class Position:
    func: Callable[..., NDArray]
    params: Dict[str, Any]
    curried: Callable[..., NDArray] = field(init=False)

    def __post_init__(self) -> Callable[..., NDArray]:
        self.curried =  partial(self.func, **self.params)

@dataclass
class Sensor:
    id: str 
    type_id: str 

@dataclass
class Source:
    id: str
    type_id: str 
