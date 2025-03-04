# base/experiment_setup.py
from dataclasses import dataclass
from typing import List, Dict, Any
import numpy as np
from base.experiment import Experiment
from base.field import Source, Sensor

@dataclass
class ExperimentSetup:
    """Dataclass to hold the complete experiment setup."""
    experiment: Experiment
    sources: List[Source]
    sensors: List[Sensor]
    paths: Dict[str, np.ndarray] # Optional: Keep paths for now for potential use