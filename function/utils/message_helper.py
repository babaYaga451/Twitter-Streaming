import json
from loguru import logger
from tweet_util import flatten_tweets, select_text, clean_tweet_text, find_centroid


def process_message(message, event_id):
    """
    process the messages received from pubsub
    cleaning the twitter data begins
    """
    logger.info("Processing messages.. event_id: {}", event_id)
    tweet_obj = json.loads(message)

    if 'place' in tweet_obj:
        tweet = {}

        tweet_obj = flatten_tweets(tweet_obj)
        tweet_obj = select_text(tweet_obj)

        tweet['text'] = clean_tweet_text(tweet_obj['text'])
        tweet['created_at'] = tweet_obj['created_at']
        tweet['user_screen_name'] = tweet_obj['user_screen_name']
        tweet['user_name'] = tweet_obj['user_name']
        tweet['country_code'] = tweet_obj['place-country_code']
        tweet['country'] = tweet_obj['place-country']

        if 'point' == tweet_obj['location-coordinates']['type']:
            tweet['location'] = tweet_obj['location-coordinates']['coordinates']
        else:
            tweet['location'] = find_centroid(tweet_obj['location-coordinates'])

        logger.info("Formatted tweet {}", tweet)

        return tweet
