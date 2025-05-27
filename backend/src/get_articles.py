from bs4 import BeautifulSoup, ResultSet
from datetime import datetime

from pydantic import AwareDatetime

from .models import Article
from dateutil import parser
from .helpers import request_get_json, datetime_UTC, REQUEST_HEADERS, request_get_json_cached
from itertools import chain
from requests_cache import CachedSession


def get_SNAPI_articles(earliestDatetime: str) -> list[Article]:
    '''Return extracted industry news articles from SNAPI.'''

    # Get industry space news articles from SNAPI call
    url = 'https://api.spaceflightnewsapi.net/v4/articles'
    # published_at_gte refers to all documents published after a given ISO8601 timestamp (included)
    params = {'published_at_gte': earliestDatetime, 'limit': 20}
    with CachedSession() as session:
        results = request_get_json_cached(url, session, params=params)

        # Paginate through all the results of query
        items = []
        if results and 'results' in results:
            nextURL = results.get('next')
            while nextURL:
                # Requesting next data
                nextResults = request_get_json(nextURL)
                # Adding to the original results dictionary
                results['results'] += nextResults['results']
                # Updating the next URL
                nextURL = nextResults.get('next')
            items = results['results']

    # Extract data from results
    articles = [Article(title=item['title'],
                        content=item['summary'],
                        author=item['news_site'],
                        image=item['image_url'],
                        url=item['url'],
                        timestamp=datetime.fromisoformat(
                            item['published_at']).timestamp(),
                        category='Industry')
                for item in items]
    return articles


def get_physorg_articles(earliestDatetime: AwareDatetime) -> list[Article]:
    '''Scrapes phys.org RSS feeds and returns a list of articles.'''

    def _get_physorg_items(url: str, session: CachedSession) -> ResultSet:
        '''Extracts articles from a given phys.org RSS feed.'''
        # Get RSS Feed items
        res = session.get(url, headers=REQUEST_HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'xml')
        items = soup.find_all('item')
        return items

    # Extract articles from RSS feeds
    with CachedSession() as session:
        astrobiologyItems = _get_physorg_items(
            'https://phys.org/rss-feed/space-news/astrobiology', session)
        astronomyItems = _get_physorg_items(
            'https://phys.org/rss-feed/space-news/astronomy', session)
        planetarySciItems = _get_physorg_items(
            'https://phys.org/rss-feed/space-news/planetary-sciences', session)
    items = chain(astrobiologyItems, astronomyItems, planetarySciItems)

    # Extract data from items
    articleDict = {}
    earliest = datetime_UTC(earliestDatetime)
    for item in items:
        # Skip if article has already been extracted
        if item.guid.text in articleDict:
            continue
        # Skip 'Space Exploration' articles
        category = item.category.text.strip()
        if 'Space Exploration' in category:
            continue
        # Skip article if before earliest datetime (NO DB YET)
        dt = datetime_UTC(parser.parse(item.pubDate.text))
        if dt < earliest:
            continue
        ts = dt.timestamp()
        # Extract data for articles
        title = item.title.text.strip()
        content = item.description.text.strip()
        author = 'phys.org'
        url = item.link.text
        image = item.thumbnail['url']
        article = Article(title=title,
                          content=content,
                          author=author,
                          image=image,
                          url=url,
                          timestamp=ts,
                          category=category)
        articleDict[item.guid.text] = article
    articles = articleDict.values()
    return articles


def get_industry_articles(earliestDatetime: AwareDatetime, limit: int | None = None):
    '''Aggregates and returns space industry news articles.'''
    SNAPIArticles = get_SNAPI_articles(earliestDatetime)
    articles = list(chain(SNAPIArticles))
    return sorted(articles,
                  key=lambda x: x.timestamp,
                  reverse=True)[:limit]


def get_science_articles(earliestDatetime: AwareDatetime, limit: int | None = None) -> list[Article]:
    '''Aggregates and returns space science news articles.'''
    physOrgArticles = get_physorg_articles(earliestDatetime)
    articles = list(chain(physOrgArticles))
    return sorted(articles,
                  key=lambda x: x.timestamp,
                  reverse=True)[:limit]


def get_all_articles(earliestDatetime: AwareDatetime, limit: int | None = None):
    '''Aggregates and returns all space news articles.'''
    industryArticles = get_industry_articles(earliestDatetime)
    scienceArticles = get_science_articles(earliestDatetime)
    articles = list(chain(industryArticles, scienceArticles))
    return sorted(articles,
                  key=lambda x: x.timestamp,
                  reverse=True)[:limit]
