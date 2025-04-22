from typing import Annotated
from fastapi import APIRouter, Query

from datetime import date

from src.models import EPICAPICollectionType, EPICAPIImageType, EPICImage
from src.get_imagery import get_EPIC_API_images

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
    '''Returns images of Earth from NASA's EPIC API.'''
    print(collection, series, image_type, image_date)

    images = get_EPIC_API_images(
        collection.value, series, image_type.value, image_date)
    return images
