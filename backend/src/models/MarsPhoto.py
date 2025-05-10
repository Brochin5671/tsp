from dataclasses import dataclass
from enum import StrEnum, auto


class MarsPhotoRoverType(StrEnum):
    '''Enum for Mars Photo API rover type.'''
    CURIOSITY: str = auto()
    SPIRIT: str = auto()
    OPPORTUNITY: str = auto()
    PERSEVERANCE: str = auto()
    ACTIVE: str = 'active'
    INACTIVE: str = 'inactive'
    ALL: str = 'all'  # TODO: group rovers


class MarsPhotoCameraType(StrEnum):
    '''Enum for Mars Photo API camera type.'''
    FHAZ: str = auto(),
    NAVCAM: str = auto(),
    MAST: str = auto(),
    CHEMCAM: str = auto(),
    MAHLI: str = auto(),
    MARDI: str = auto(),
    RHAZ: str = auto(),
    MAST_LEFT: str = auto(),
    MAST_RIGHT: str = auto(),
    CHEMCAM_RMI: str = auto(),
    FHAZ_LEFT_B: str = auto(),
    FHAZ_RIGHT_B: str = auto(),
    NAV_LEFT_B: str = auto(),
    NAV_RIGHT_B: str = auto(),
    RHAZ_LEFT_B: str = auto(),
    RHAZ_RIGHT_B: str = auto(),
    PANCAM: str = auto(),
    MINITES: str = auto(),
    ENTRY: str = auto(),
    EDL_RUCAM: str = auto(),
    EDL_DDCAM: str = auto(),
    EDL_PUCAM1: str = auto(),
    EDL_PUCAM2: str = auto(),
    NAVCAM_LEFT: str = auto(),
    NAVCAM_RIGHT: str = auto(),
    MCZ_RIGHT: str = auto(),
    MCZ_LEFT: str = auto(),
    FRONT_HAZCAM_LEFT_A: str = auto(),
    FRONT_HAZCAM_RIGHT_A: str = auto(),
    REAR_HAZCAM_LEFT: str = auto(),
    REAR_HAZCAM_RIGHT: str = auto(),
    EDL_RDCAM: str = auto(),
    SKYCAM: str = auto(),
    SHERLOC_WATSON: str = auto(),
    SUPERCAM_RMI: str = auto(),
    LCAM: str = auto()


@dataclass(kw_only=True)
class MarsPhotoCamera:
    '''Dataclass for Mars rover camera names.'''
    short: str
    name: str


@dataclass
class MarsRover:
    '''Dataclass for Mars rover metadata from `mars_rovers.json`.'''
    name: str
    launch_date: str
    landing_date: str
    active: bool
    cameras: list[MarsPhotoCamera]
    final_sol: int | None = None
    final_date: str | None = None
    total_photos: int | None = None


@dataclass(kw_only=True)
class MarsPhotoMetadataManifest:
    '''Dataclass for extracted Mars rover manifest data from the Mars Photo API.'''
    sol: int
    earth_date: str
    total_photos: int
    cameras: list[MarsPhotoCamera]


@dataclass(kw_only=True)
class MarsPhotoMetadata:
    '''Dataclass for extracted Mars rover metadata from the Mars Photo API.'''
    rover: MarsRover
    manifests: list[MarsPhotoMetadataManifest] | None = None


@dataclass(kw_only=True)
class MarsPhoto:
    '''Dataclass for extracted image metadata from the Mars Photo API.'''
    rover_name: str
    camera: MarsPhotoCamera
    image: str
    earth_date: str
    sol: int
