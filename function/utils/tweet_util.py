import re
from geojson_utils import centroid


def clean_tweet_text(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Remove @Mentions
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)  # Remove RT
    text = re.sub(r'https?:\/\/\S+', '', text)  # Remove hyperlink
    return text


def find_centroid(polygon):
    return centroid(polygon)['coordinates']
