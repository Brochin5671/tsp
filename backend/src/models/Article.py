from dataclasses import dataclass


@dataclass
class Article:
    '''Dataclass for news articles.'''
    title: str
    content: str
    author: str
    image: str
    url: str
    timestamp: float
    category: str
