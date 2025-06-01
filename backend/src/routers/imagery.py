from collections import deque
from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, status

from datetime import date

from src.models import EPICAPICollectionType, EPICAPIImageType, EPICAPIImage, MarsPhotoAPIRoverType, MarsPhotoAPICameraType, MarsPhotoAPIImage, MARS_PHOTO_API_DATA
from src.apis import get_EPIC_API_images, get_mars_photo_API_images, get_mars_photo_API_metadata

router = APIRouter(prefix='/imagery', tags=['imagery'])


def _remove_rover_flags(rovers: set[MarsPhotoAPIRoverType]):
    '''Removes flags and updates the rover set.'''
    # Modify rover set used for querying if flags were used
    used_flags = rovers & MarsPhotoAPIRoverType.get_flags()

    # Don't modify rover set
    if not used_flags:
        return rovers

    # Add all rovers
    if MarsPhotoAPIRoverType.ALL in used_flags:
        return MarsPhotoAPIRoverType.get_rovers()

    # Remove flags from rover set
    rovers -= used_flags

    # Add active and/or inactive rovers to rover set
    if MarsPhotoAPIRoverType.ACTIVE in used_flags:
        rovers |= MarsPhotoAPIRoverType.get_active_rovers()
    if MarsPhotoAPIRoverType.INACTIVE in used_flags:
        rovers |= MarsPhotoAPIRoverType.get_inactive_rovers()

    return rovers


@router.get('/epic')
async def get_EPIC_API(
    collection: Annotated[EPICAPICollectionType, Query(
        description='Kind of imagery to return: natural or enhanced, aersol index, or cloud fraction imagery.')] = EPICAPICollectionType.NATURAL,
    series: Annotated[bool, Query(
        description='To return a series or a single image. Will return the latest of the series if single.')] = False,
    image_type: Annotated[EPICAPIImageType, Query(
        description='Image type for imagery resolution.')] = EPICAPIImageType.PNG,
    image_date: Annotated[date, Query(
        description='A date string in ISO 8601 format: YYYY-MM-DD',
        alias='date')] = None
) -> deque[EPICAPIImage]:
    '''Returns images of Earth from NASA's EPIC API.
    The EPIC API provides information on the daily imagery collected by DSCOVR's Earth Polychromatic Imaging Camera (EPIC) instrument. Uniquely positioned at the Earth-Sun Lagrange point, EPIC provides full disc imagery of the Earth and captures unique perspectives of certain astronomical events such as lunar transits using a 2048x2048 pixel CCD (Charge Coupled Device) detector coupled to a 30-cm aperture Cassegrain telescope. The API is maintained by the NASA EPIC Team. https://epic.gsfc.nasa.gov/about/api'''

    # Try to get images from EPIC API
    try:
        images = get_EPIC_API_images(
            collection, series, image_type, image_date)
    except Exception as e:
        print(e)  # TODO: logging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong on our end, please try again later.')

    return images


@router.get('/mars-photo')
async def get_mars_photo_API(
    rovers: Annotated[set[MarsPhotoAPIRoverType], Query(
        description='Filter for photos from specific rovers.')] = MarsPhotoAPIRoverType.get_rovers(),
    cameras: Annotated[set[MarsPhotoAPICameraType], Query(
        description='Filter for photos from specific rover cameras (picks from a specific day).')] = None,
    earth_date: Annotated[date, Query(
        description='A date string in ISO 8601 format "YYYY-MM-DD", starting from the landing date up to the current maximum earth date. If both earth_date and sol aren\'t specified, latest image data is returned.')] = None,
    sol: Annotated[int, Query(
        description='The Martian sol (Martian day) starting from the landing date up to the current maximum sol. If both earth_date and sol aren\'t specified, latest image data is returned.',
        ge=0)] = None
) -> deque[MarsPhotoAPIImage]:
    '''Returns images from Mars rovers using the Mars Photo API.
    The Mars Photo API is designed to collect image data gathered by NASA's Curiosity, Opportunity, Spirit, and Perseverance rovers on Mars and make it more easily available to other developers, educators, and citizen scientists. This API is maintained by Chris Cerami. https://mars-photos.herokuapp.com/explore/'''

    # Modify rover set used for querying if flags were used
    rovers = _remove_rover_flags(rovers)

    # Check if selected cameras are in any selected rover
    if cameras:
        # Get all cameras from all selected rovers as a set
        rover_cameras = set()
        rover_configs = MARS_PHOTO_API_DATA['rovers'].items()
        for rover_name, rover_values in rover_configs:
            if rover_name in rovers:
                rover_cameras |= rover_values['cameras']
        # Filter out cameras by intersecting selected and all camera sets
        result = cameras & rover_cameras
        # Return not found if no selected cameras in any selected rover
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'There are no selected cameras in any of the selected rovers')

    # Try to get images from Mars Photo API
    try:
        images = get_mars_photo_API_images(rovers, cameras, earth_date, sol)
    except Exception as e:
        print(e)  # TODO: logging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong on our end, please try again later.')

    return images


@router.get('/mars-photo/meta')
async def get_mars_photo_API_metadata(
    rovers: Annotated[set[MarsPhotoAPIRoverType], Query(
        description='Filter for metadata from specific rovers.')] = MarsPhotoAPIRoverType.get_rovers(),
    manifest: Annotated[bool, Query(
        description='To return photo manifests with metadata.')] = None,
    earth_date: Annotated[date, Query(
        description='A date string in ISO 8601 format "YYYY-MM-DD", starting from the landing date up to the current maximum earth date. If both earth_date and sol aren\'t specified, latest image data is returned.')] = None,
    sol: Annotated[int, Query(
        description='The Martian sol (Martian day) starting from the landing date up to the current maximum sol. If both earth_date and sol aren\'t specified, latest image data is returned.',
        ge=0)] = None
):
    '''Returns metadata from Mars rovers (optionally photo manifests) using the Mars Photo API.
    The Mars Photo API is designed to collect image data gathered by NASA's Curiosity, Opportunity, Spirit, and Perseverance rovers on Mars and make it more easily available to other developers, educators, and citizen scientists. This API is maintained by Chris Cerami. https://mars-photos.herokuapp.com/explore/'''

    # Modify rover set used for querying if flags were used
    rovers = _remove_rover_flags(rovers)

    # Try to get metadata from Mars Photo API
    try:
        metadata = get_mars_photo_API_metadata(
            rovers, manifest, earth_date, sol)
    except Exception as e:
        print(e)  # TODO: logging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong on our end, please try again later.')

    return metadata
