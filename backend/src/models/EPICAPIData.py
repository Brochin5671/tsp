from dataclasses import dataclass
from enum import StrEnum, auto
from typing import NamedTuple


class EPICAPIGeoCoordinate(NamedTuple):
    '''Class for centroid coordinates.'''
    lat: float
    lon: float


class EPICAPI3DCoordinate(NamedTuple):
    '''Class for j2000 object positions.'''
    x: float
    y: float
    z: float


@dataclass(kw_only=True)
class EPICAPIQuaternions:
    '''Class for object attitude quaternions.'''
    q0: float
    q1: float
    q2: float
    q3: float


class EPICAPICollectionType(StrEnum):
    '''Enum for EPIC API collection type.'''
    NATURAL: str = auto()
    ENHANCED: str = auto()
    AEROSOL: str = auto()
    CLOUD: str = auto()


class EPICAPIImageType(StrEnum):
    '''Enum for EPIC API image type.'''
    PNG: str = auto()
    JPG: str = auto()
    THUMBS: str = auto()


@dataclass(kw_only=True)
class EPICAPIImage:
    '''Dataclass for extracted image metadata from the EPIC API.'''
    image: str
    timestamp: float
    dscovr_view_coordinates: EPICAPIGeoCoordinate
    dscovr_j2000_position: EPICAPI3DCoordinate
    lunar_j2000_position: EPICAPI3DCoordinate
    sun_j2000_position: EPICAPI3DCoordinate
    dscovr_attitude: EPICAPIQuaternions
