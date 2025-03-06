from dataclasses import dataclass, field
from typing import List, Dict, Any
import numpy as np
from numpy.typing import NDArray
from numpy.lib.stride_tricks import sliding_window_view as swv
import scipy.stats as stats
from base import *
from utils.functional import f_kwargs 
from utils.math import compute_all_distances, naive_path_integral, _slicer
from utils.attenuation import inv_sql

@dataclass
class Observed:
    locations: List[NDArray] = field(default_factory=list)
    readings: NDArray = field(default_factory=lambda: np.array([]))


@dataclass
class Latent:
    distances: NDArray = field(default_factory=lambda: np.array([]))
    ev_source: NDArray = field(default_factory=lambda: np.array([]))
    ev_background: NDArray = field(default_factory=lambda: np.array([]))
    signal_s: NDArray = field(default_factory=lambda: np.array([]))
    signal_b: NDArray = field(default_factory=lambda: np.array([]))

@dataclass
class Experiment:
    id:str = None
    sensors: List[Sensor] = field(default_factory=list)
    sources: List[Source] = field(default_factory=list)
    positions:List[Position] = field(default_factory=list)
    length: float = field(default=100.0)
    hz: float = field(default=10.0)
    trials: int = field(default=1)
    dt: float = field(init=False)
    steps: int = field(init=False)
    time_points: NDArray = field(init=False)
    observed: Observed = field(default_factory=Observed)
    latent: Latent = field(default_factory=Latent)
    obs_shape: Tuple = field(init=False)

    def __post_init__(self) -> None:
        """Initialize time-related parameters after constructor."""
        self.dt = 1.0 / self.hz
        self.steps = int(self.length * self.hz)
        self.time_points = np.linspace(0, self.length, self.steps+1)
        self.obs_shape = (self.trials, len(self.sensors), int(self.length))

    def run(self) -> List[Dict[str, Any]]:
        """Run the experiment simulation."""
        # ... (simulation logic later)
        pos_map = lambda : [f_kwargs(p.curried, self.__dict__)for p in self.positions][0]
        dist_map = lambda : compute_all_distances(*(pos_map()))
    
        background = StatsRV('toy', stats.gengamma, dict(a=0.75, c = 2.6, loc=0, scale= 0.4625))
        rv = StatsRV('toy', stats.norm)
        dl = Dilution('toy', inv_sql, {'strength': 10, 'scale':7})
        f_param  =  lambda x: {'loc': x, 'scale': .2*x}
        _distances = lambda : naive_path_integral(lambda x: x, dist_map()) 
        latent_params = f_param(dl.curried(_distances()))
        print(dist_map().shape, pos_map().shape)
        self.latent.distances = _distances()
        self.latent.ev_source= latent_params['loc']
        self.latent.ev_background = np.zeros_like(self.latent.distances) + background.mean()
        self.latent.signal_s= stats.norm(**latent_params).rvs()
        self.latent.signal_b= background.sample(self.obs_shape)
        self.observed.locations = _slicer(swv(pos_map(), window_shape = 11, axis = 1), 10,1).mean(axis = -1)
        self.observed.readings = self.latent.signal_b + self.latent.signal_s

        