from collections import deque
from datetime import date
import json
from dateutil import parser
from requests_cache import CachedSession

from src.helpers import datetime_UTC, request_get_json_cached
from src.models import EPICAPICollectionType, EPICAPIImageType, EPICAPIImage, MarsPhotoAPICamera, MarsPhotoAPIRover, MarsPhotoAPIRoverType, MarsPhotoAPICameraType, MarsPhotoAPICamera, MarsPhotoAPIImage, MarsPhotoAPIMetadataManifest, MarsPhotoAPIMetadata, EPICAPIGeoCoordinate, EPICAPI3DCoordinate, EPICAPIQuaternions


def get_EPIC_API_images(collection: EPICAPICollectionType, series: bool, image_type: EPICAPIImageType, image_date: date | None) -> deque[EPICAPIImage]:
    '''Returns images of Earth from NASA's EPIC API.'''

    # Call EPIC API
    url = f'https://epic.gsfc.nasa.gov/api/{collection}'
    # Add date route if given
    if image_date is not None:
        url += f'/date/{image_date}'
    with CachedSession() as session:
        res = request_get_json_cached(url, session)

    # Return an empty deque if response is empty
    if not res:
        return deque()

    # Get all items if user requested a series
    if series:
        data = res
    else:
        data = [res[-1]]  # Latest of series

    # Extract data from image items
    images = deque()
    for item in data:
        # Format of date in item will always be "YYYY-MM-DD HH:MM:SS"
        year = item['date'][:4]
        month = item['date'][5:7]
        day = item['date'][8:10]
        # To get the URL of an image: https://epic.gsfc.nasa.gov/archive/(natural|enhanced|aersol|cloud)/YYYY/MM/DD/(png|jpg|thumbs)/<filename>
        image_url = f"https://epic.gsfc.nasa.gov/archive/{collection}/{year}/{month}/{day}/{image_type}/{item['image']}.{image_type}"
        # Create objects
        ts = datetime_UTC(parser.parse(item['date'])).timestamp()
        sat_view = EPICAPIGeoCoordinate(**item['centroid_coordinates'])
        sat_pos = EPICAPI3DCoordinate(**item['dscovr_j2000_position'])
        lunar_pos = EPICAPI3DCoordinate(**item['lunar_j2000_position'])
        sun_pos = EPICAPI3DCoordinate(**item['sun_j2000_position'])
        sat_attitude = EPICAPIQuaternions(**item['attitude_quaternions'])
        image = EPICAPIImage(image=image_url,
                             timestamp=ts,
                             dscovr_view_coordinates=sat_view,
                             dscovr_j2000_position=sat_pos,
                             lunar_j2000_position=lunar_pos,
                             sun_j2000_position=sun_pos,
                             dscovr_attitude=sat_attitude)
        images.append(image)

    return images


def _load_mars_rovers_json(rovers_only: bool = False) -> tuple[dict[str, str], dict[str, str] | None]:
    '''Tries to load and return JSON data from the `mars_rovers.json` file.'''
    # Try to load file, raises missing file or key errors on failure
    with open('./src/data/mars_rovers.json') as file:
        data = json.load(file)

    # Raise error if file is just "{}"
    if not data:
        raise RuntimeError('"mars_rovers.json" is missing data.')

    # Raise error if "rovers" is just "{}"
    rovers_data = data['rovers']
    if not rovers_data:
        raise RuntimeError('"mars_rovers.json" is missing rover data.')
    # Return just rover data if specified
    if rovers_only:
        return rovers_data, None

    # Raise error if "cameras" is just "{}"
    camera_mappings = data['cameras']
    if not camera_mappings:
        raise RuntimeError(
            '"mars_rovers.json" is missing camera mappings data.')
    return rovers_data, camera_mappings


def get_mars_photos_API_images(rovers: set[MarsPhotoAPIRoverType], cameras: set[MarsPhotoAPICameraType] | None, earth_date: date | None, sol: int | None) -> deque[MarsPhotoAPIImage]:
    '''Returns images from Mars rovers using the Mars Photo API.'''

    # If earth_date and sol weren't provided, get latest photos
    endpoint = 'photos'
    if earth_date is None and sol is None:
        endpoint = 'latest_photos'

    # Query data from rovers
    params = {'earth_date': earth_date, 'sol': sol}
    images = deque()
    with CachedSession() as session:
        for rover in rovers:

            # Get set of cameras to filter for
            filter_cameras = None
            if cameras:
                # Get JSON data
                rovers_data, _ = _load_mars_rovers_json(rovers_only=True)
                # Intersect given cameras and a rover's available cameras
                rover_cameras = {camera.lower()
                                 for camera in rovers_data[rover]['cameras']}
                filter_cameras = cameras & rover_cameras

            # Call API if no cameras were provided or there are cameras to filter for
            if not cameras or filter_cameras:
                url = f'https://mars-photos.herokuapp.com/api/v1/rovers/{rover}/{endpoint}'
                res = request_get_json_cached(url, session, params=params)
                data = res[endpoint]

                # Extract data from image items
                for item in data:

                    # Skip item if there are cameras to filter for and item's camera is not in filter
                    item_camera = item['camera']
                    camera_short = item_camera['name']
                    if cameras and camera_short.lower() not in filter_cameras:
                        continue

                    # Create objects
                    camera_obj = MarsPhotoAPICamera(short=camera_short,
                                                    name=item_camera['full_name'])
                    image = MarsPhotoAPIImage(rover_name=item['rover']['name'],
                                              camera=camera_obj,
                                              image=item['img_src'],
                                              earth_date=item['earth_date'],
                                              sol=item['sol'])
                    images.append(image)

    return images


def get_mars_photos_API_metadata(rovers: set[MarsPhotoAPIRoverType], manifest: bool | None, earth_date: date | None, sol: int | None) -> deque[MarsPhotoAPIMetadata]:
    '''Returns metadata from Mars rovers (optionally photo manifests) using the Mars Photo API.'''

    # Get JSON data
    rovers_data, camera_mappings = _load_mars_rovers_json()

    # Return metadata on requested rovers
    metadata_list = deque()
    with CachedSession() as session:
        for rover in rovers:
            rover_data = rovers_data[rover]

            # Extract camera short and full names
            cameras = [MarsPhotoAPICamera(short=camera_short, name=camera_mappings[camera_short])
                       for camera_short in rover_data['cameras']]
            rover_data['cameras'] = cameras
            # Create metadata objects
            rover_obj = MarsPhotoAPIRover(**rover_data)
            metadata = MarsPhotoAPIMetadata(rover=rover_obj)

            # Add rover manifest to metadata if requested
            if manifest:
                url = f'https://mars-photos.herokuapp.com/api/v1/manifests/{rover}'
                res = request_get_json_cached(url, session)

                # Filter for specific manifests if earth_date or sol provided
                if earth_date:
                    data = [item for item in res['photo_manifest']['photos']
                            if item['earth_date'] == earth_date.isoformat()]
                elif sol is not None:
                    data = [item for item in res['photo_manifest']['photos']
                            if item['sol'] == sol]
                else:
                    data = res['photo_manifest']['photos']

                # Extract data from manifest items
                manifests = deque()
                for item in data:
                    # Extract camera short and full name from manifest item
                    manifest_cameras = [MarsPhotoAPICamera(short=camera_short, name=camera_mappings[camera_short])
                                        for camera_short in item['cameras']]
                    item['cameras'] = manifest_cameras
                    manifest = MarsPhotoAPIMetadataManifest(**item)
                    manifests.append(manifest)
                metadata.manifests = manifests

            # If rover is still active, update fields to reflect current values
            if rover_obj.active:
                url = f'https://mars-photos.herokuapp.com/api/v1/rovers/{rover}'
                res = request_get_json_cached(url, session)
                data = res['rover']
                rover_obj.final_date = data['max_date']
                rover_obj.final_sol = data['max_sol']
                rover_obj.total_photos = data['total_photos']

            metadata_list.append(metadata)

    return metadata_list
