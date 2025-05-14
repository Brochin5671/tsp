from datetime import datetime, UTC, timedelta
from pydantic import AwareDatetime
import requests
from requests_cache import CachedSession
from typing import Any, Callable

REQUEST_HEADERS: dict[str, str] = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}


def noop(*args, **kwargs) -> None:
    pass


def request_get_json(
        url: str,
        params: dict[str, Any] | None = None,
        *,
        exception_handler: Callable[[requests.RequestException], Any] = noop,
        headers: dict[str, Any] | None = None,
        timeout: int = 10
) -> Any:
    """Handles a GET request and returns the json-encoded content of a response, if any.
        Args:
            url (str): URL for the new `Request` object.
            params (dict[str, Any]): Optional. A list of tuples or bytes to send in the query string for the `Request`.
            exception_fn (Callable[[RequestException], Any]): Optional. A function that takes in the `RequestException` and returns json-encoded content, if any.
            headers (dict[str, Any]): Optional. A dictionary of HTTP headers to send to the specified url.
            timeout (int): Optional. A number indicating how many seconds to wait for the client to make a connection and/or send a response.
    """
    data = None
    try:
        res = requests.get(url, params, headers=headers, timeout=timeout)
        res.raise_for_status()
        data = res.json()
    except requests.exceptions.RequestException as e:
        data = exception_handler(e)
    return data


def request_get_json_cached(
        url: str,
        session: CachedSession,
        *,
        params: dict[str, Any] | None = None,
        exception_handler: Callable[[requests.RequestException], Any] = noop,
        headers: dict[str, Any] | None = None,
        timeout: int = 10
) -> Any:
    """Handles a GET request and returns the json-encoded content of a response, if any.
        Args:
            url (str): URL for the new `Request` object.
            session (CachedSession): a cached version of a `Session` object for making requests.
            params (dict[str, Any]): Optional. A list of tuples or bytes to send in the query string for the `Request`.
            exception_fn (Callable[[RequestException], Any]): Optional. A function that takes in the `RequestException` and returns json-encoded content, if any.
            headers (dict[str, Any]): Optional. A dictionary of HTTP headers to send to the specified url.
            timeout (int): Optional. A number indicating how many seconds to wait for the client to make a connection and/or send a response.
    """
    data = None
    try:
        res = session.get(url, params, headers=headers, timeout=timeout)
        res.raise_for_status()
        data = res.json()
    except requests.exceptions.RequestException as e:
        data = exception_handler(e)
    return data


def datetime_UTC(dt: datetime) -> AwareDatetime:
    '''Sets a datetime object's timezone to UTC.'''
    if dt.tzinfo is None:
        # Assume naive datetime is UTC
        return dt.replace(tzinfo=UTC)
    else:
        # Convert any aware datetime to UTC
        return dt.astimezone(UTC)


def datetime_UTC_Week() -> AwareDatetime:
    '''Returns the datetime a week ago in UTC.'''
    return datetime.now(UTC) - timedelta(days=7)
