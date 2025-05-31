from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import AwareDatetime

from src.helpers import datetime_UTC_Week
from src.models import Article
from src.apis import get_all_articles, get_industry_articles, get_science_articles

router = APIRouter(prefix='/news', tags=['news'])


@router.get('/')
async def get_space_news(
        earliest_datetime: Annotated[AwareDatetime, Query(
            description="ISO-8601 timezone-aware datetime string for returning articles after this datetime.")] = datetime_UTC_Week(),
        limit: Annotated[int, Query(
            description="Amount of articles to return.",
            ge=0)] = 10
) -> list[Article]:
    '''Returns articles on space industry and/or science news.'''
    # Try to get articles
    try:
        articles = get_all_articles(earliest_datetime, limit)
    except Exception as e:
        print(e)  # TODO: logging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong on our end, please try again later.')

    return articles


@router.get('/industry')
async def get_space_industry_news(
        earliest_datetime: Annotated[AwareDatetime, Query(
            description="ISO-8601 timezone-aware datetime string for returning articles after this datetime.")] = datetime_UTC_Week(),
        limit: Annotated[int, Query(
            description="Amount of articles to return.",
            ge=0)] = 10
) -> list[Article]:
    '''Returns articles on space industry news.'''
    # Try to get articles
    try:
        articles = get_industry_articles(earliest_datetime, limit)
    except Exception as e:
        print(e)  # TODO: logging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong on our end, please try again later.')

    return articles


@router.get('/science')
async def get_space_science_news(
        earliest_datetime: Annotated[AwareDatetime, Query(
            description="ISO-8601 timezone-aware datetime string for returning articles after this datetime.")] = datetime_UTC_Week(),
        limit: Annotated[int, Query(
            description="Amount of articles to return.",
            ge=0)] = 10
) -> list[Article]:
    '''Returns articles on space science news.'''
    # Try to get articles
    try:
        articles = get_science_articles(earliest_datetime, limit)
    except Exception as e:
        print(e)  # TODO: logging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong on our end, please try again later.')

    return articles
