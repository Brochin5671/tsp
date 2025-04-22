from datetime import date
import requests
from dateutil import parser

from src.helpers import datetime_UTC, request_get_json
from src.models import EPICAPICollectionType, EPICAPIImageType, EPICImage

# KEY = os.getenv('NASA_API_KEY')
KEY = 'DEMO_KEY'


def get_EPIC_API_images(collection: EPICAPICollectionType, series: bool, image_type: EPICAPIImageType, image_date: date | None) -> list[EPICImage]:
    '''The EPIC API provides information on the daily imagery collected by DSCOVR's Earth Polychromatic Imaging Camera (EPIC) instrument. Uniquely positioned at the Earth-Sun Lagrange point, EPIC provides full disc imagery of the Earth and captures unique perspectives of certain astronomical events such as lunar transits using a 2048x2048 pixel CCD (Charge Coupled Device) detector coupled to a 30-cm aperture Cassegrain telescope. This function is intended to return images and their metadata.'''

    # Exception handler for EPIC API call
    def handle_EPIC_API_exception(e):
        '''Returns an empty list on failure.'''
        print(e)  # TODO: logging
        return []

    # Call EPIC API
    url = f'https://epic.gsfc.nasa.gov/api/{collection}'
    if image_date is not None:
        url += f'/date/{image_date}'
    res = request_get_json(url, exception_handler=handle_EPIC_API_exception)
    # Return an empty list if failure to get data
    if not res:
        return []

    # Get all items if user requested a series
    if series:
        items = res
    else:
        items = [res[-1]]  # latest of series

    # To get the URL of the image: https://epic.gsfc.nasa.gov/archive/(natural|enhanced|aersol|cloud)/YYYY/MM/DD/(png|jpg|thumbs)/<filename>
    images = []
    for item in items:
        # Format of date in item will always be "YYYY-MM-DD HH:MM:SS"
        year = item['date'][:4]
        month = item['date'][5:7]
        day = item['date'][8:10]
        image_url = f"https://epic.gsfc.nasa.gov/archive/{collection}/{year}/{month}/{day}/{image_type}/{item['image']}.{image_type}"
        ts = datetime_UTC(parser.parse(item['date'])).timestamp()

        image = EPICImage(
            image=image_url, timestamp=ts, **item['coords'])
        images.append(image)
    return images
