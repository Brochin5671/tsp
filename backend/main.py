from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware

import os

from src.routers import news

# Setup app
PROD = os.getenv('PROD')
DEV = os.getenv('DEV')
description = '''
### API for all things space
Space news, epihermes, other info and more!
'''
version = '0.3.0 (v1)'
docs_url = '/docs'
app = FastAPI(title='The Space Prime API',
              description=description,
              summary=None,
              version=version,
              docs_url=docs_url,
              redoc_url=None,
              openapi_url='/schema',
              terms_of_service=None,
              contact={
                  "name": "Maxim Brochin",
                  "url": "https://www.maximbrochin.com",
                  "email": "",
              },
              license_info={
                  "name": "MIT License",
                  "identifier": "MIT",
              },
              )
app.include_router(news.router, responses={
                   429: {
                       'content': {
                           'application/json': {
                               'example': {
                                   'error': 'Rate limit exceeded: 10 per 1 second'
                               }
                           }
                       }
                   }}
                   )

# Setup rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=['10/second'])
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore
app.add_middleware(SlowAPIMiddleware)

# Setup middlewares
if PROD:
    app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(GZipMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['*'])
