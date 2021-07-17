"""
All configuration required for this project
"""

from tweepy import OAuthHandler
from os import environ
from google.cloud import pubsub_v1

consumer_key = environ.get('CONSUMER_KEY')
consumer_secret = environ.get('CONSUMER_SECRET')
access_token = environ.get('ACCESS_TOKEN')
access_token_secret = environ.get('ACCESS_TOKEN_SECRET')


def get_auth():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth


def get_publisher_client():
    publisher = pubsub_v1.PublisherClient()
    return publisher
