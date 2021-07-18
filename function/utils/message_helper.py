import base64
import json
from loguru import logger
from .tweet_util import clean_tweet_text, find_centroid


def process_message(message, event_id):
    """
    process the messages received from pubsub
    cleaning the twitter data begins
    """
    logger.info("Processing messages.. event_id: {}", event_id)
    message = base64.b64decode(message).decode('utf-8')
    tweet_obj = json.loads(message)
    logger.info("Type {} tweet_obj {}", type(tweet_obj), tweet_obj)

    if tweet_obj['place'] or tweet_obj['coordinates']:
        tweet = {}

        if tweet_obj['truncated']:
            tweet['text'] = tweet_obj['extended_tweet']['full_text']
        tweet['text'] = clean_tweet_text(tweet_obj['text'])
        tweet['created_at'] = tweet_obj['created_at']
        tweet['user_screen_name'] = tweet_obj['user']['screen_name']
        tweet['user_name'] = tweet_obj['user']['name']
        tweet['country_code'] = tweet_obj['place']['country_code']
        tweet['country'] = tweet_obj['place']['country']

        if tweet_obj['coordinates']:
            tweet['location'] = tweet_obj['coordinates']['coordinates']
        elif tweet_obj['place']:
            tweet['location'] = find_centroid(tweet_obj['place']['bounding_box'])

        logger.info("Formatted tweet {}", tweet)

        return tweet
