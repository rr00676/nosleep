# base/field_objects.py
from typing import Protocol, runtime_checkable, Optional
from base.attenuation import AttenuatorProtocol # Import here after defining SourceProtocol to avoid circular dependency during type checking
from base.distribution import DistributionProtocol # Import here after defining SourceProtocol to avoid circular dependency during type checking
from dataclasses import dataclass


@runtime_checkable
class FieldObjectProtocol(Protocol):
    """Base protocol for field objects (Sensors, Sources)."""
    pass # location might be added later if needed

@runtime_checkable
class SourceProtocol(FieldObjectProtocol, Protocol):
    """Protocol for signal sources."""
    attenuator: AttenuatorProtocol # Attenuation model for the source signal
    distribution: DistributionProtocol # Distribution of the signal emitted by the source

@runtime_checkable
class SensorProtocol(FieldObjectProtocol, Protocol):
    """Protocol for sensors."""
    # Sensors are placeholders for now, can add specific attributes later
    pass

@dataclass
class FieldObj:
    """Base dataclass for field objects."""
    pass # location could be added here later if needed

@dataclass
class Source(FieldObj, SourceProtocol):
    """Concrete class for signal sources."""
    attenuator: Optional[AttenuatorProtocol] = None
    distribution: Optional[DistributionProtocol] = None

@dataclass
class Sensor(FieldObj, SensorProtocol):
    """Concrete class for sensors."""
    pass # Sensor properties can be added later