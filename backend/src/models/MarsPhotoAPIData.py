from collections import deque
from dataclasses import InitVar, dataclass, field
from enum import StrEnum, auto
from functools import cached_property
from typing import Self

MARS_PHOTO_API_DATA = {
    'rovers': {
        'curiosity': {
            'name': 'Curiosity',
            'launch_date': '2011-11-26',
            'landing_date': '2012-08-06',
            'active': True,
            'camera_names': {
                'fhaz',
                'navcam',
                'mast',
                'chemcam',
                'mahli',
                'mardi',
                'rhaz',
                'mast_left',
                'mast_right',
                'chemcam_rmi',
                'fhaz_left_b',
                'fhaz_right_b',
                'nav_left_b',
                'nav_right_b',
                'rhaz_left_b',
                'rhaz_right_b'
            }
        },
        'spirit': {
            'name': 'Spirit',
            'launch_date': '2003-06-1',
            'landing_date': '2004-01-04',
            'active': False,
            'camera_names': {'fhaz', 'navcam', 'pancam', 'minites', 'entry', 'rhaz'},
            'current_sol': 2208,
            'current_date': '2010-03-21',
            'total_photos': 124550
        },
        'opportunity': {
            'name': 'Opportunity',
            'launch_date': '2003-07-07',
            'landing_date': '2004-01-25',
            'active': False,
            'camera_names': {'fhaz', 'navcam', 'pancam', 'minites', 'entry', 'rhaz'},
            'current_sol': 5111,
            'current_date': '2018-06-11',
            'total_photos': 198439
        },
        'perseverance': {
            'name': 'Perseverance',
            'launch_date': '2020-07-30',
            'landing_date': '2021-02-18',
            'active': True,
            'camera_names': {
                'edl_rucam',
                'edl_ddcam',
                'edl_pucam1',
                'edl_pucam2',
                'navcam_left',
                'navcam_right',
                'mcz_right',
                'mcz_left',
                'front_hazcam_left_a',
                'front_hazcam_right_a',
                'rear_hazcam_left',
                'rear_hazcam_right',
                'edl_rdcam',
                'skycam',
                'sherloc_watson',
                'supercam_rmi',
                'lcam'
            }
        }
    },
    'cameras': {
        'FHAZ': 'Front Hazard Avoidance Camera',
        'NAVCAM': 'Navigation Camera',
        'MAST': 'Mast Camera',
        'CHEMCAM': 'Chemistry and Camera Complex',
        'MAHLI': 'Mars Hand Lens Imager',
        'MARDI': 'Mars Descent Imager',
        'RHAZ': 'Rear Hazard Avoidance Camera',
        'MAST_LEFT': 'Mast Camera - Left',
        'MAST_RIGHT': 'Mast Camera - Right',
        'CHEMCAM_RMI': 'Chemistry and Camera Complex Remote Micro Imager',
        'FHAZ_LEFT_B': 'Front Hazard Avoidance Camera - Left',
        'FHAZ_RIGHT_B': 'Front Hazard Avoidance Camera - Right',
        'NAV_LEFT_B': 'Navigation Camera - Left',
        'NAV_RIGHT_B': 'Navigation Camera - Right',
        'RHAZ_LEFT_B': 'Rear Hazard Avoidance Camera - Left',
        'RHAZ_RIGHT_B': 'Rear Hazard Avoidance Camera - Right',
        'PANCAM': 'Panoramic Camera',
        'MINITES': 'Miniature Thermal Emission Spectrometer (Mini-TES)',
        'ENTRY': 'Entry, Descent, and Landing Camera',
        'EDL_RUCAM': 'Rover Up-Look Camera',
        'EDL_DDCAM': 'Descent Stage Down-Look Camera',
        'EDL_PUCAM1': 'Parachute Up-Look Camera A',
        'EDL_PUCAM2': 'Parachute Up-Look Camera B',
        'NAVCAM_LEFT': 'Navigation Camera - Left',
        'NAVCAM_RIGHT': 'Navigation Camera - Right',
        'MCZ_RIGHT': 'Mast Camera Zoom - Right',
        'MCZ_LEFT': 'Mast Camera Zoom - Left',
        'FRONT_HAZCAM_LEFT_A': 'Front Hazard Avoidance Camera - Left',
        'FRONT_HAZCAM_RIGHT_A': 'Front Hazard Avoidance Camera - Right',
        'REAR_HAZCAM_LEFT': 'Rear Hazard Avoidance Camera - Left',
        'REAR_HAZCAM_RIGHT': 'Rear Hazard Avoidance Camera - Right',
        'EDL_RDCAM': 'Rover Down-Look Camera',
        'SKYCAM': 'MEDA Skycam',
        'SHERLOC_WATSON': 'SHERLOC WATSON Camera',
        'SUPERCAM_RMI': 'SuperCam Remote Micro Imager',
        'LCAM': 'Lander Vision System Camera'
    }
}


class MarsPhotoAPIRoverType(StrEnum):
    '''Enum for Mars Photo API rover type.'''
    ALL: str = auto()
    ACTIVE: str = auto()
    INACTIVE: str = auto()
    CURIOSITY: str = auto()
    SPIRIT: str = auto()
    OPPORTUNITY: str = auto()
    PERSEVERANCE: str = auto()

    @classmethod
    def get_flags(cls) -> set[Self]:
        return {cls.ALL, cls.ACTIVE, cls.INACTIVE}

    @classmethod
    def get_active_rovers(cls) -> set[Self]:
        return {cls.CURIOSITY, cls.PERSEVERANCE}

    @classmethod
    def get_inactive_rovers(cls) -> set[Self]:
        return {cls.SPIRIT, cls.OPPORTUNITY}

    @classmethod
    def get_rovers(cls) -> set[Self]:
        return {cls.CURIOSITY, cls.SPIRIT, cls.OPPORTUNITY, cls.PERSEVERANCE}


class MarsPhotoAPICameraType(StrEnum):
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
class MarsPhotoAPICamera:
    '''Dataclass for Mars rover camera names.'''
    short: str
    name: str


@dataclass(kw_only=True)
class MarsPhotoAPIRover:
    '''Dataclass for Mars rover metadata.'''
    name: str
    launch_date: str
    landing_date: str
    active: bool
    camera_names: InitVar[set[str]]
    cameras: list[MarsPhotoAPICamera] = field(init=False)
    current_sol: int | None = None
    current_date: str | None = None
    total_photos: int | None = None

    def __post_init__(self, camera_names):
        # Grabs camera_names and creates a MarsPhotoAPICamera list
        camera_mappings = MARS_PHOTO_API_DATA['cameras']
        self.cameras = [MarsPhotoAPICamera(
            short=short.upper(),
            name=camera_mappings[short.upper()]) for short in camera_names]

    @cached_property
    def camera_shorts(self):
        '''A set of a rover's camera short names.'''
        return {camera.short for camera in self.cameras}


MARS_PHOTO_API_ROVERS = {}
for name, data in MARS_PHOTO_API_DATA['rovers'].items():
    MARS_PHOTO_API_ROVERS[name] = MarsPhotoAPIRover(**data)


@dataclass(kw_only=True)
class MarsPhotoAPIMetadataManifest:
    '''Dataclass for extracted Mars rover manifest data from the Mars Photo API.'''
    sol: int
    earth_date: str
    total_photos: int
    cameras: list[MarsPhotoAPICamera]


@dataclass(kw_only=True)
class MarsPhotoAPIMetadata:
    '''Dataclass for extracted Mars rover metadata from the Mars Photo API.'''
    rover: MarsPhotoAPIRover
    manifests: deque[MarsPhotoAPIMetadataManifest] | None = None


@dataclass(kw_only=True)
class MarsPhotoAPIImage:
    '''Dataclass for extracted image metadata from the Mars Photo API.'''
    rover_name: str
    camera: MarsPhotoAPICamera
    image: str
    earth_date: str
    sol: int
