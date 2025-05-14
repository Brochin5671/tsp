from collections import deque
from datetime import date
import json
from dateutil import parser
from requests_cache import CachedSession

from src.helpers import datetime_UTC, request_get_json, request_get_json_cached
from src.models import EPICAPICollectionType, EPICAPIImageType, EPICImage, MarsPhotoAPICamera, MarsRover, MarsPhotoAPIRoverType, MarsPhotoAPICameraType, MarsPhotoAPICamera, MarsPhotoAPIImage, MarsPhotoAPIMetadataManifest, MarsPhotoAPIMetadata


def get_EPIC_API_images(collection: EPICAPICollectionType, series: bool, image_type: EPICAPIImageType, image_date: date | None) -> list[EPICImage]:
    '''Returns images of Earth from NASA's EPIC API.'''

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


def _get_mars_rovers_json() -> dict:
    '''Returns the JSON data from the mars_rovers.json file.'''
    data = {}
    with open('./src/data/mars_rovers.json') as file:
        data = json.load(file)
    return data


def _handle_mars_photos_API_exception(e):
    '''Returns an empty dictionary on failure.'''
    print(e)  # TODO: logging and exception handling
    return {}


def get_mars_photos_API_images(rovers: set[MarsPhotoAPIRoverType], cameras: set[MarsPhotoAPICameraType] | None, earth_date: date | None, sol: int | None) -> deque[MarsPhotoAPIImage]:
    '''Returns a list of photos from Mars rovers using the Mars Photo API.'''

    # Get JSON data
    json_data = _get_mars_rovers_json()
    rovers_data = json_data.get('rovers', {})

    # If earth_date and sol weren't provided, get latest photos
    endpoint = 'photos'
    if earth_date is None and sol is None:
        endpoint = 'latest_photos'

    # Query data from rovers
    session = CachedSession()
    params = {'earth_date': earth_date, 'sol': sol}
    photos = deque()
    for rover in rovers:

        # Get set of cameras to filter for by intersecting given cameras and a rover's available cameras
        rover_cameras = {camera.lower()
                         for camera in rovers_data[rover]['cameras']}
        filter_cameras = cameras & rover_cameras if cameras else None

        # Call API if no cameras were provided or there are cameras to filter for
        if not cameras or filter_cameras:
            url = f'https://mars-photos.herokuapp.com/api/v1/rovers/{rover}/{endpoint}'
            res = request_get_json_cached(
                url, session, params=params, exception_handler=_handle_mars_photos_API_exception)
            data = res[endpoint]

            # Extract data
            for item in data:

                # Skip item if there are cameras to filter for and item's camera is not in filter
                item_camera = item['camera']
                camera_short = item_camera['name']
                if cameras and camera_short.lower() not in filter_cameras:
                    continue

                # Create camera object
                camera_obj = MarsPhotoAPICamera(short=camera_short,
                                                name=item_camera['full_name'])
                # Create photo object
                photo = MarsPhotoAPIImage(rover_name=item['rover']['name'],
                                          camera=camera_obj,
                                          image=item['img_src'],
                                          earth_date=item['earth_date'],
                                          sol=item['sol'])
                photos.append(photo)
    session.close()
    return photos


def get_mars_photos_api_metadata(rovers: set[MarsPhotoAPIRoverType], manifest: bool | None) -> list[MarsPhotoAPIMetadata]:
    '''Returns a list of Mars Rover metadata (optionally photo manifests) using the Mars Photo API.'''

    # Get JSON data
    json_data = _get_mars_rovers_json()
    rovers_data = json_data.get('rovers', {})
    camera_mappings = json_data.get('cameras', {})

    # Return metadata on requested rovers
    session = CachedSession()
    metadata_list = []
    for rover in rovers:
        rover_data = rovers_data[rover]
        # Extract camera short and full names
        cameras = [MarsPhotoAPICamera(short=camera_short, name=camera_mappings[camera_short])
                   for camera_short in rover_data['cameras']]
        rover_data['cameras'] = cameras
        # Create rover metadata object
        rover_obj = MarsRover(**rover_data)
        metadata = MarsPhotoAPIMetadata(rover=rover_obj)

        # Add rover manifest to metadata if requested
        if manifest:
            url = f'https://mars-photos.herokuapp.com/api/v1/manifests/{rover}'
            res = request_get_json_cached(
                url, session, exception_handler=_handle_mars_photos_API_exception)
            data = res['photo_manifest']

            # Extract data from manifest items
            manifest_list = []
            for item in data['photos']:
                # Extract camera short and full name from manifest item
                manifest_cameras = [MarsPhotoAPICamera(short=camera_short, name=camera_mappings[camera_short])
                                    for camera_short in item['cameras']]
                item['cameras'] = manifest_cameras
                manifest_obj = MarsPhotoAPIMetadataManifest(**item)
                manifest_list.append(manifest_obj)
            metadata.manifests = manifest_list

        # If rover is still active, update fields to reflect current values
        if rover_obj.active:
            url = f'https://mars-photos.herokuapp.com/api/v1/rovers/{rover}'
            res = request_get_json_cached(
                url, session, exception_handler=_handle_mars_photos_API_exception)
            data = res['rover']
            rover_obj.final_date = data['max_date']
            rover_obj.final_sol = data['max_sol']
            rover_obj.total_photos = data['total_photos']

        metadata_list.append(metadata)
    session.close()
    return metadata_list
