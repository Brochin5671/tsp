from datetime import date
import json
from dateutil import parser

from src.helpers import datetime_UTC, request_get_json
from src.models import EPICAPICollectionType, EPICAPIImageType, EPICImage, MarsPhotoCamera, MarsRover, MarsPhotoRoverType, MarsPhotoCameraType, MarsPhotoCamera, MarsPhoto, MarsPhotoMetadataManifest, MarsPhotoMetadata


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


def get_mars_photos_API_images(rovers: list[MarsPhotoRoverType], cameras: list[MarsPhotoCameraType] | None, earth_date: date | None, sol: int | None) -> list[MarsPhoto]:
    '''Returns a list of photos from Mars rovers using the Mars Photo API.'''

    # Get JSON data
    json_data = _get_mars_rovers_json()
    rovers_data = json_data.get('rovers', {})
    camera_mappings = json_data.get('cameras', {})

    # If earth_date and sol weren't provided, get latest photos
    endpoint = 'photos'
    if earth_date is None and sol is None:
        endpoint = 'latest_photos'

    # Query data from rovers
    photos: list[MarsPhoto] = []  # TODO: list -> deque
    for rover in rovers:
        url = f'https://mars-photos.herokuapp.com/api/v1/rovers/{rover}/{endpoint}'
        params = {'earth_date': earth_date, 'sol': sol}
        # Query camera data individually if selected
        if cameras:
            for camera in cameras:
                # Check if rover has given camera to reduce calls
                camera_short = camera.upper()
                rover_cameras = rovers_data.get(rover, {}).get('cameras', [])
                if camera_short in rover_cameras:
                    # Set camera param prior to API call
                    params['camera'] = camera
                    res = request_get_json(
                        url, params, exception_handler=_handle_mars_photos_API_exception)
                    data = res[endpoint]
                    # Extract photo data
                    for item in data:
                        # Create camera object
                        camera_name = camera_mappings.get(camera_short)
                        camera_obj = MarsPhotoCamera(short=camera_short,
                                                     name=camera_name)
                        # Create photo object
                        photo = MarsPhoto(rover_name=item['rover']['name'],
                                          camera=camera_obj,
                                          image=item['img_src'],
                                          earth_date=item['earth_date'],
                                          sol=item['sol'])
                        photos.append(photo)
        else:
            res = request_get_json(
                url, params, exception_handler=_handle_mars_photos_API_exception)
            data = res[endpoint]
            # Extract photo data
            for item in data:
                # Create camera object
                camera_short = item['camera']['name']
                camera_name = camera_mappings.get(camera_short)
                camera_obj = MarsPhotoCamera(short=camera_short,
                                             name=camera_name)
                # Create photo object
                photo = MarsPhoto(rover_name=item['rover']['name'],
                                  camera=camera_obj,
                                  image=item['img_src'],
                                  earth_date=item['earth_date'],
                                  sol=item['sol'])
                photos.append(photo)

    return photos


def get_mars_photos_api_metadata(rovers: list[MarsPhotoRoverType], manifest: bool | None) -> list[MarsPhotoMetadata]:
    '''Returns a list of Mars Rover metadata (optionally photo manifests) using the Mars Photo API.'''

    # Get JSON data
    json_data = _get_mars_rovers_json()
    rovers_data = json_data.get('rovers', {})
    camera_mappings = json_data.get('cameras', {})

    # Return metadata on requested rovers
    metadata_list = []
    for rover in rovers:
        rover_data = rovers_data[rover]
        # Extract camera short and full names
        cameras = [MarsPhotoCamera(short=camera_short, name=camera_mappings[camera_short])
                   for camera_short in rover_data['cameras']]
        rover_data['cameras'] = cameras
        # Create rover metadata object
        rover_obj = MarsRover(**rover_data)
        metadata = MarsPhotoMetadata(rover=rover_obj)

        # Add rover manifest to metadata if requested
        if manifest:
            url = f'https://mars-photos.herokuapp.com/api/v1/manifests/{rover}'
            res = request_get_json(
                url, exception_handler=_handle_mars_photos_API_exception)
            data = res['photo_manifest']

            # Extract data from manifest items
            manifest_list = []
            for item in data['photos']:
                # Extract camera short and full name from manifest item
                manifest_cameras = [MarsPhotoCamera(short=camera_short, name=camera_mappings[camera_short])
                                    for camera_short in item['cameras']]
                item['cameras'] = manifest_cameras
                manifest_obj = MarsPhotoMetadataManifest(**item)
                manifest_list.append(manifest_obj)
            metadata.manifests = manifest_list

        # If rover is still active, update fields to reflect current values
        if rover_obj.active:
            url = f'https://mars-photos.herokuapp.com/api/v1/rovers/{rover}'
            res = request_get_json(
                url, exception_handler=_handle_mars_photos_API_exception)
            data = res['rover']
            rover_obj.final_date = data['max_date']
            rover_obj.final_sol = data['max_sol']
            rover_obj.total_photos = data['total_photos']

        metadata_list.append(metadata)
    return metadata_list
