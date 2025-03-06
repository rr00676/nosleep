"""Builder module for creating Experiment instances from configuration."""
import numpy as np
from numpy.typing import NDArray
from typing import Any, Dict, List, Callable, Optional, Tuple
from dataclasses import dataclass, field

import utils.motion as motion
from base import *
from experiment import *

# Registry mapping function names to actual functions
POSITION_FUNCTIONS = {
    "Linear": motion.linear,
    "Stationary": motion.stationary,
    "Elliptical": motion.elliptical,
    "RandomWalk": motion.random_walk
}

def get_position_func(func_name: str) -> Callable[..., NDArray]:
    """Return a position function based on name."""
    if func_name in POSITION_FUNCTIONS:
        return POSITION_FUNCTIONS[func_name]
    else:
        raise ValueError(f"Unknown position function: {func_name}")


class ExperimentBuilder:
    """Builder for constructing Experiment objects from configuration."""
    
    def __init__(self):
        """Initialize builder with empty configurations."""
        self.sensor_configs: List[Dict[str, Any]] = []
        self.source_configs: List[Dict[str, Any]] = []
        self.positions: List[Position] = []
        self.sensors: List[Sensor] = []
        self.sources: List[Source] = []
        self.timing_config: Dict[str, Any] = {}


    def add_timings(self, config: Dict[str, Any]) -> None:
        """Add timing parameters to the builder."""
        self.timing_config = config
    
    def add_sensor_config(self, config: Dict[str, Any]) -> None:
        """Add a sensor configuration to the builder."""
        self.sensor_configs.append(config)
    
    def add_source_config(self, config: Dict[str, Any]) -> None:
        """Add a source configuration to the builder."""
        self.source_configs.append(config)

    def _build_sensors(self) -> List[Sensor]:
        """Build sensors from stored configurations."""
        self.sensors = []
        
        for config in self.sensor_configs:
            count = config.get('count', 1)
            sensor_type = config.get('type', 'simple')
            position_func_name = config.get('position_func', 'Stationary')
            position_args = config.get('position_args', {})
            
            # Get the position function
            position_func = get_position_func(position_func_name)
            self.positions.append(Position(func=position_func, params=position_args))
            
            
            for i in range(count):
                # Create sensor-specific position arguments
                sensor_position_args = {}
                for key, value in position_args.items():
                    if isinstance(value, list) and len(value) > 0:
                        # Handle cases where we have a list of parameters for each sensor
                        if isinstance(value[0], list) and i < len(value):
                            sensor_position_args[key] = value[i]
                        elif not isinstance(value[0], list) and len(value) > i:
                            sensor_position_args[key] = value[i]
                        else:
                            sensor_position_args[key] = value[0]
                    else:
                        sensor_position_args[key] = value
        
                sensor = Sensor(id=f"{sensor_type}_{i}", type_id=sensor_type)
                self.sensors.append(sensor)
            
    def _build_sources(self) -> List[Source]:
        """Build sources from stored configurations."""
        
        for config in self.source_configs:
            count = config.get('count', 1)
            source_type = config.get('type', 'simple')
            position_func_name = config.get('position_func', 'Stationary')
            position_args = config.get('position_args', {})
            
            # Get the position function
            position_func = get_position_func(position_func_name)
            self.positions.append(Position(func=position_func, params=position_args))
            
            for i in range(count):
                # Create source-specific position arguments
                source_position_args = {}
                for key, value in position_args.items():
                    if isinstance(value, list) and len(value) > 0:
                        # Handle cases where we have a list of parameters for each source
                        if isinstance(value[0], list) and i < len(value):
                            source_position_args[key] = value[i]
                        elif not isinstance(value[0], list) and len(value) > i:
                            source_position_args[key] = value[i]
                        else:
                            source_position_args[key] = value[0]
                    else:
                        source_position_args[key] = value
                source = Source(
                    id=f"{source_type}_{i}",
                    type_id=source_type,
                )
                
                self.sources.append(source)
        
    
    def build_experiment(self) -> Experiment:
        """Build experiment from stored configurations."""
        # Extract timing parameters
        length = float(self.timing_config.get('length', 100.0))
        hz = float(self.timing_config.get('hz', 10.0))
        trials = int(self.timing_config.get('trials', 1))
        
        self._build_sensors()
        self._build_sources()
        
        return Experiment(sensors=self.sensors, 
                          sources=self.sources, 
                          positions= self.positions, 
                          length=length, 
                          hz=hz, 
                          trials=trials, 
                          observed = Observed(),
                          latent = Latent()
                          )

        
        