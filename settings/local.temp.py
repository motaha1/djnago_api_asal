from .base import *
import os

DEBUG = True
ENVIRONMENT = "LOCAL"
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# psycopg2-2.9.5-cp38-cp38-win_amd64.whl

# --------------------  DataBase Config  --------------#
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'askcaredb-local-v2',
#         'USER': 'postgresAdmin',
#         'PASSWORD': 'care@#@#2020',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

# --------------------  AWS SDK Keys  --------------#

AWS_ACCESS_KEY_ID = "AKIAZFAVUAA5S3CS4COV"
AWS_SECRET_ACCESS_KEY = "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"

# --------------------  Auth0 Keys  --------------#

AUTH0_DOMAIN_URL = "https://askcare-live.eu.auth0.com"
AUTH0_CLIENT_ID = "pIaL42r1uWkRj9eysDVAA8sgOuX9xjnK"
AUTH0_CLIENT_SECRET = "icuzyF69OTlWewJnO5M9OWZ5yyVUCSA3J-36d6Aqlj504yf8eLoDHEaGcjqgerkB"
AUTH0_API_ENDPOINT_URL = f"{AUTH0_DOMAIN_URL}/api/v2"
AUTH0_FETCH_TOKEN_API_URL = f"{AUTH0_DOMAIN_URL}/oauth/token"

# --------------------  Cache config  --------------#

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-cache'
    }
}