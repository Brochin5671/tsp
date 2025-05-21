from datetime import date
from typing import Any
from src.models import EPICAPICollectionType, EPICAPIImageType, MarsPhotoAPIRoverType, MarsPhotoAPICameraType
import src.get_imagery as get_imagery
from unittest.mock import patch
import pytest


@pytest.fixture
def collection_arg() -> EPICAPICollectionType:
    return EPICAPICollectionType.NATURAL


@pytest.fixture
def series_arg() -> bool | None:
    return False


@pytest.fixture
def image_type_arg() -> EPICAPIImageType:
    return EPICAPIImageType.THUMBS


@pytest.fixture
def image_date_arg() -> date | None:
    return None


@pytest.fixture
def get_EPIC_API_images_args(collection_arg: EPICAPICollectionType, series_arg: bool, image_type_arg: EPICAPIImageType, image_date_arg: date | None) -> dict[str, Any]:
    return {'collection': collection_arg,
            'series': series_arg,
            'image_type': image_type_arg,
            'image_date': image_date_arg}


@pytest.fixture
def rovers_arg() -> set[MarsPhotoAPIRoverType]:
    return MarsPhotoAPIRoverType.get_inactive_rovers()


@pytest.fixture
def cameras_arg() -> set[MarsPhotoAPICameraType] | None:
    return None


@pytest.fixture
def earth_date_arg() -> date | None:
    return None


@pytest.fixture
def sol_arg() -> int | None:
    return None


@pytest.fixture
def get_mars_photos_API_images_args(rovers_arg: set[MarsPhotoAPIRoverType], cameras_arg: set[MarsPhotoAPICameraType] | None, earth_date_arg: date | None, sol_arg: int | None) -> dict[str, Any]:
    return {'rovers': rovers_arg,
            'cameras': cameras_arg,
            'earth_date': earth_date_arg,
            'sol': sol_arg}


@pytest.fixture
def manifest_arg() -> bool | None:
    return False


@pytest.fixture
def get_mars_photos_API_metadata_args(rovers_arg: set[MarsPhotoAPIRoverType], manifest_arg: bool | None, earth_date_arg: date | None, sol_arg: int | None) -> dict[str, Any]:
    return {'rovers': rovers_arg,
            'manifest': manifest_arg,
            'earth_date': earth_date_arg,
            'sol': sol_arg}


@pytest.mark.parametrize(
    'series_arg, image_date_arg',
    [(True, None),
     (False, None),
     (False, date(year=2025, month=5, day=18))]
)
def test_get_EPIC_API_images(get_EPIC_API_images_args):
    # Verify function can call API and return images
    images = get_imagery.get_EPIC_API_images(**get_EPIC_API_images_args)
    assert images, '"get_EPIC_API_images()" must return a non-empty deque.'
    collection, series, image_type, image_date = get_EPIC_API_images_args.values()
    # Verify correct collection type is used
    assert not any(
        collection not in image.image for image in images), f'Incorrect collection type was used. {images=}'
    # Verify if one or more images are returned if specified
    images_len = len(images)
    assert images_len > 1 if series else images_len == 1, f"Length of deque should be {'greater than ' if series else 'equal to '}1."
    # Verify correct image type is used
    assert not any(
        image_type not in image.image for image in images), f'Incorrect image type was used. {images=}'
    # Verify correct date is used if passed
    if image_date is not None:
        # Convert timestamp because time is included in data
        assert not any(
            date.fromtimestamp(image.timestamp) != image_date for image in images), f'Incorrect image_date was used. {images=}'''


@patch('src.get_imagery.request_get_json_cached')
def test_get_EPIC_API_images_empty_response(mock_EPIC_API, get_EPIC_API_images_args):
    mock_EPIC_API.return_value = []
    images = get_imagery.get_EPIC_API_images(**get_EPIC_API_images_args)
    assert not images, '"get_EPIC_API_images()" must return an empty deque.'


@pytest.mark.parametrize(
    'cameras_arg, earth_date_arg, sol_arg',
    [(None, None, None),
     ({MarsPhotoAPICameraType.PANCAM}, None, 1000),
     ({MarsPhotoAPICameraType.SHERLOC_WATSON}, None, 1000),
     (None, date(year=2006, month=10, day=27), None)]
)
def test_get_mars_photos_API_images(get_mars_photos_API_images_args):
    # Verify function can call API and return images
    images = get_imagery.get_mars_photos_API_images(
        **get_mars_photos_API_images_args)
    rovers, cameras, earth_date, sol = get_mars_photos_API_images_args.values()
    # Verify correct rover type is used
    assert not any(
        image.rover_name.lower() not in rovers for image in images), f'Incorrect rover type was used. {images=}'
    # Verify correct camera type is used if given
    if cameras:
        # For specific test parameter, deque must be empty
        if MarsPhotoAPICameraType.SHERLOC_WATSON in cameras:
            assert not images, '"get_mars_photo_API_images()" must return an empty deque.'
        else:
            assert not any(
                image.camera.short.lower() not in cameras for image in images), f'Incorrect camera type was used. {images=}'
    # Verify correct earth date is used if passed
    if earth_date is not None:
        assert not any(image.earth_date !=
                       str(earth_date) for image in images), f'Incorrect earth date was used. {images=}'
    # Verify correct sol is used if passed
    if sol is not None:
        assert not any(
            image.sol != sol for image in images), f'Incorrect sol was used. {images=}'


@pytest.mark.parametrize(
    'rovers_arg, manifest_arg, earth_date_arg, sol_arg',
    [(MarsPhotoAPIRoverType.get_active_rovers(), False, None, None),
     (MarsPhotoAPIRoverType.get_inactive_rovers(), True, None, 1000),
     (MarsPhotoAPIRoverType.get_inactive_rovers(),
      True, date(year=2006, month=10, day=27), None),
     ({MarsPhotoAPIRoverType.SPIRIT}, True, None, None)]
)
def test_get_mars_photos_API_metadata(get_mars_photos_API_metadata_args):
    # Verify function can call API and return metadata
    metadata_list = get_imagery.get_mars_photos_API_metadata(
        **get_mars_photos_API_metadata_args)
    rovers, manifest, earth_date, sol = get_mars_photos_API_metadata_args.values()
    # Verify correct rover type is used
    assert not any(
        metadata.rover.name.lower() not in rovers for metadata in metadata_list), f'Incorrect rover type was used. {metadata_list=}'
    # Verify manifests are used
    if manifest:
        # Verify correct earth date or sol is used if passed
        if earth_date is not None:
            assert not any(manifest.earth_date != str(earth_date)
                           for metadata in metadata_list
                           for manifest in metadata.manifests), f'Incorrect earth date was used. {metadata_list=}'
        elif sol is not None:
            assert not any(manifest.sol != sol
                           for metadata in metadata_list
                           for manifest in metadata.manifests), f'Incorrect sol was used. {metadata_list=}'
        else:
            for metadata in metadata_list:
                assert metadata.manifests, f'Manifest must be a non-empty deque. {metadata=}'
