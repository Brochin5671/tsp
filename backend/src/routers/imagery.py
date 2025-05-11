from typing import Annotated
from fastapi import APIRouter, Query

from datetime import date

from src.models import EPICAPICollectionType, EPICAPIImageType, EPICImage, MarsPhotoRoverType, MarsPhotoCameraType, MarsPhoto
from src.get_imagery import get_EPIC_API_images, get_mars_photos_API_images, get_mars_photos_api_metadata

router = APIRouter(prefix='/imagery', tags=['imagery'])


@router.get('/epic')
async def get_EPIC_API(
    collection: Annotated[EPICAPICollectionType, Query(
        description='Kind of imagery to return: natural or enhanced, aersol index, or cloud fraction imagery.')] = EPICAPICollectionType.NATURAL,
    series: Annotated[bool, Query(
        description='To return a series or a single image. Will return the latest of the series if single.')] = None,
    image_type: Annotated[EPICAPIImageType, Query(
        description='Image type for imagery resolution.')] = EPICAPIImageType.PNG,
    image_date: Annotated[date, Query(
        description='A date string in ISO 8601 format: YYYY-MM-DD',
        alias='date')] = None
) -> list[EPICImage]:
    '''Returns images of Earth from NASA's EPIC API.
    The EPIC API provides information on the daily imagery collected by DSCOVR's Earth Polychromatic Imaging Camera (EPIC) instrument. Uniquely positioned at the Earth-Sun Lagrange point, EPIC provides full disc imagery of the Earth and captures unique perspectives of certain astronomical events such as lunar transits using a 2048x2048 pixel CCD (Charge Coupled Device) detector coupled to a 30-cm aperture Cassegrain telescope. This function is intended to return images and their metadata.'''
    images = get_EPIC_API_images(
        collection, series, image_type, image_date)
    return images


@router.get('/mars-photo')
async def get_mars_photos(
    rovers: Annotated[set[MarsPhotoRoverType], Query(
        description='Filter for photos from specific rovers.')],
    cameras: Annotated[set[MarsPhotoCameraType], Query(
        description='Filter for photos from specific rover cameras (picks from a specific day).')] = None,
    earth_date: Annotated[date, Query(
        description='A date string in ISO 8601 format "YYYY-MM-DD", starting from the landing date up to the current maximum earth date. If both earth_date and sol aren\'t specified, latest image data is returned.')] = None,
    sol: Annotated[int, Query(
        description='The Martian sol (Martian day) starting from the landing date up to the current maximum sol. If both earth_date and sol aren\'t specified, latest image data is returned.',
        ge=0)] = None
) -> list[MarsPhoto]:
    '''Returns a list of photos from Mars rovers using the Mars Photo API.
    The Mars Photo API is designed to collect image data gathered by NASA's Curiosity, Opportunity, Spirit, and Perseverance rovers on Mars and make it more easily available to other developers, educators, and citizen scientists. This API is maintained by Chris Cerami. https://mars-photos.herokuapp.com/explore/'''
    # TODO: error checking with date and sol
    images = get_mars_photos_API_images(rovers, cameras, earth_date, sol)
    return images


@router.get('/mars-photo/meta')
async def get_mars_photos_metadata(
    rovers: Annotated[set[MarsPhotoRoverType], Query(
        description='Filter for metadata from specific rovers.')],
    manifest: Annotated[bool, Query(
        description='To return photo manifests with metadata.')] = None
):
    '''Returns a list of Mars Rover metadata (optionally photo manifests) using the Mars Photo API.
    The Mars Photo API is designed to collect image data gathered by NASA's Curiosity, Opportunity, Spirit, and Perseverance rovers on Mars and make it more easily available to other developers, educators, and citizen scientists. This API is maintained by Chris Cerami. https://mars-photos.herokuapp.com/explore/'''
    metadata = get_mars_photos_api_metadata(rovers, manifest)
    return metadata
