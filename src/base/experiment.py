# base/experiment.py
from dataclasses import dataclass, field
from typing import List, Dict, Any
import numpy as np

@dataclass
class Experiment:
    """Dataclass to hold experiment parameters."""
    duration: float # total experiment duration in seconds
    hz: float # sensor sampling rate in Hz
    trials: int # number of experiment trials
    steps: int = field(init=False) # total number of steps
    dt: float = field(init=False) # time step duration
    time_points: np.ndarray = field(init=False) # array of time points

    def __post_init__(self):
        """Calculates steps, dt, and time_points after initialization."""
        self.steps = int(self.duration * self.hz)
        self.dt = 1.0 / self.hz
        self.time_points = np.arange(0, self.duration + self.dt, self.dt) # Include end time point