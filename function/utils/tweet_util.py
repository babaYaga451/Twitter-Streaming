import re
from geojson_utils import centroid


def flatten_tweets(tweet_obj):
    """
    flattens out the twitter dictionaries so relevant JSON
    is at top level
    """
    tweet_obj['user_screen_name'] = tweet_obj['user']['screen_name']
    tweet_obj['user_name'] = tweet_obj['user']['name']

    if 'extended_tweet' in tweet_obj:
        tweet_obj['extended_tweet-full_text'] = \
            tweet_obj['extended_tweet']['full_text']

    if 'retweeted_status' in tweet_obj:
        tweet_obj['retweeted_status-text'] = \
            tweet_obj['retweeted_status']['text']

    if 'extended_tweet' in tweet_obj['retweeted_status']:
        tweet_obj['retweeted_status-extended_tweet-full_text'] = \
            tweet_obj['retweeted_status']['extended_tweet']['full_text']

    ''' Place info'''
    if 'coordinates' in tweet_obj:
        tweet_obj['location-coordinates'] = tweet_obj['coordinates']

    elif 'place' in tweet_obj:
        # Store the country code in 'place-country_code'
        try:
            tweet_obj['place-country'] = \
                tweet_obj['place']['country']

            tweet_obj['place-country_code'] = \
                tweet_obj['place']['country_code']

            tweet_obj['location-coordinates'] = \
                tweet_obj['place']['bounding_box']
        except:
            pass

    return tweet_obj


def select_text(tweet_obj):
    if 'retweeted_status-extended_tweet-full_text' in tweet_obj:
        tweet_obj['text'] = \
            tweet_obj['retweeted_status-extended_tweet-full_text']

    elif 'retweeted_status-text' in tweet_obj:
        tweet_obj['text'] = tweet_obj['retweeted_status-text']

    elif 'extended_tweet-full_text' in tweet_obj:
        tweet_obj['text'] = tweet_obj['extended_tweet-full_text']

    return tweet_obj


def clean_tweet_text(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Remove @Mentions
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)  # Remove RT
    text = re.sub(r'https?:\/\/\S+', '', text)  # Remove hyperlink
    return text


def find_centroid(polygon):
    return centroid(polygon)['coordinates']
