from dataclasses import dataclass
from enum import StrEnum
from typing import NamedTuple


class GeoCoordinate(NamedTuple):
    '''Class for centroid coordinates.'''
    lat: float
    lon: float


class Coordinate3D(NamedTuple):
    '''Class for j2000 object positions.'''
    x: float
    y: float
    z: float


class Quaternions(NamedTuple):
    '''Class for object attitude quaternions.'''
    q0: float
    q1: float
    q2: float
    q3: float


class EPICAPICollectionType(StrEnum):
    '''Enum for EPIC API collection type.'''
    NATURAL: str = 'natural'
    ENHANCED: str = 'enhanced'
    AEROSOL: str = 'aerosol'
    CLOUD: str = 'cloud'


class EPICAPIImageType(StrEnum):
    '''Enum for EPIC API image type.'''
    PNG: str = 'png'
    JPG: str = 'jpg'
    THUMBS: str = 'thumbs'


@dataclass(kw_only=True)
class EPICImage:
    '''Dataclass for extracted image metadata from the EPIC API.'''
    image: str
    timestamp: float
    centroid_coordinates: GeoCoordinate
    dscovr_j2000_position: Coordinate3D
    lunar_j2000_position: Coordinate3D
    sun_j2000_position: Coordinate3D
    attitude_quaternions: Quaternions
