from collections import deque
from unittest.mock import patch

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from fastapi import status
import pytest

from src.models import EPICAPIImage, EPICAPIGeoCoordinate, EPICAPI3DCoordinate, EPICAPIQuaternions, MarsPhotoAPIRoverType


route = 'imagery'

'''
t1: success
t2-t_n: validation errs
t_n + 1 - t_n + m: any fn errs
'''


@pytest.fixture
def mock_get_EPIC_API_images_result():
    obj = EPICAPIImage(image='https://epic.gsfc.nasa.gov/archive/natural/2025/05/16/png/epic_1b_20250516221620.png',
                       timestamp=1747433492,
                       dscovr_view_coordinates=EPICAPIGeoCoordinate(lat=19.533691,
                                                                    lon=-165.915527),
                       dscovr_j2000_position=EPICAPI3DCoordinate(x=1058627.824999,
                                                                 y=969529.66253,
                                                                 z=507374.697954),
                       lunar_j2000_position=EPICAPI3DCoordinate(x=89979.40317,
                                                                y=-338561.221026,
                                                                z=-182907.378766),
                       sun_j2000_position=EPICAPI3DCoordinate(x=84740524.262739,
                                                              y=114969423.000052,
                                                              z=49836249.5645),
                       dscovr_attitude=EPICAPIQuaternions(q0=-0.142978,
                                                          q1=0.696068,
                                                          q2=-0.60259,
                                                          q3=0.363224))
    return deque([obj])


@pytest.fixture
def mock_get_MP_API_images_result():
    return deque([])


@pytest.fixture
def mock_get_MP_API_metadata_result():
    return deque([])


@pytest.mark.parametrize(
    'params, expected_status_code', [
        # Default call to endpoint
        (None, status.HTTP_200_OK),
        # Invalid collection type
        ({'collection': 'invalid'}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Invalid series param
        ({'series': 'invalid'}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Invalid image type
        ({'image_type': 'tiff'}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Invalid date string
        ({'date': '2019 12 1'}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Failure to get images
        (None, status.HTTP_500_INTERNAL_SERVER_ERROR)]
)
@patch('src.routers.imagery.get_EPIC_API_images')
def test_get_EPIC_API(mock_fn, mock_get_EPIC_API_images_result, client: TestClient, params, expected_status_code: int):
    # Trigger exception if expecting an internal server error
    if expected_status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        mock_fn.side_effect = Exception()
    else:
        mock_fn.return_value = mock_get_EPIC_API_images_result

    # Test endpoint
    response = client.get(f'{route}/epic', params=params)
    assert response.status_code == expected_status_code

    # Check if response is successful
    if expected_status_code == 200:
        assert response.json() == jsonable_encoder(mock_get_EPIC_API_images_result)


@pytest.mark.parametrize(
    'params, expected_status_code', [
        # Default call to endpoint
        ({'rovers': MarsPhotoAPIRoverType.CURIOSITY}, status.HTTP_200_OK),
        # Invalid rover type
        ({'rovers': 'invalid'}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Invalid camera type
        ({'rovers': MarsPhotoAPIRoverType.CURIOSITY, 'cameras': 'invalid'},
         status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Invalid earth date
        ({'rovers': MarsPhotoAPIRoverType.CURIOSITY,
         'earth_date': '2019 12 1'}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Invalid sol: greater than or equal to 0 constraint
        ({'rovers': MarsPhotoAPIRoverType.CURIOSITY, 'sol': -1},
         status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Invalid sol
        ({'rovers': MarsPhotoAPIRoverType.CURIOSITY, 'sol': 'invalid'},
         status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Failure to get images
        ({'rovers': MarsPhotoAPIRoverType.CURIOSITY}, status.HTTP_500_INTERNAL_SERVER_ERROR)]
)
@patch('src.routers.imagery.get_MP_API_images')
def test_get_mars_photo_API(mock_fn, mock_get_MP_API_images_result, client, params, expected_status_code):
    # Trigger exception if expecting an internal server error
    if expected_status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        mock_fn.side_effect = Exception()
    else:
        mock_fn.return_value = mock_get_MP_API_images_result

    # Test endpoint
    response = client.get(f'{route}/mars-photo', params=params)
    assert response.status_code == expected_status_code

    # Check if response is successful
    if expected_status_code == 200:
        assert response.json() == jsonable_encoder(
            mock_get_MP_API_images_result)


@pytest.mark.parametrize(
    'params, expected_status_code', [
        # Default call to endpoint
        ({'rovers': MarsPhotoAPIRoverType.SPIRIT}, status.HTTP_200_OK),
        # Invalid rover type
        ({'rovers': 'invalid'}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Invalid manifest param
        ({'rovers': MarsPhotoAPIRoverType.SPIRIT, 'manifest': 'invalid'},
         status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Invalid earth date
        ({'rovers': MarsPhotoAPIRoverType.SPIRIT,
         'earth_date': '2019 12 1'}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Invalid sol: greater than or equal to 0 constraint
        ({'rovers': MarsPhotoAPIRoverType.SPIRIT, 'sol': -1},
         status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Invalid sol
        ({'rovers': MarsPhotoAPIRoverType.SPIRIT, 'sol': 'invalid'},
         status.HTTP_422_UNPROCESSABLE_ENTITY),
        # Failure to get metadata
        ({'rovers': MarsPhotoAPIRoverType.SPIRIT}, status.HTTP_500_INTERNAL_SERVER_ERROR)]
)
@patch('src.routers.imagery.get_MP_API_metadata')
def test_get_mars_photo_API_metadata(mock_fn, mock_get_MP_API_metadata_result, client, params, expected_status_code):
    # Trigger exception if expecting an internal server error
    if expected_status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        mock_fn.side_effect = Exception()
    else:
        mock_fn.return_value = mock_get_MP_API_metadata_result

    # Test endpoint
    response = client.get(f'{route}/mars-photo/meta', params=params)
    assert response.status_code == expected_status_code

    # Check if response is successful
    if expected_status_code == 200:
        assert response.json() == jsonable_encoder(
            mock_get_MP_API_metadata_result)
