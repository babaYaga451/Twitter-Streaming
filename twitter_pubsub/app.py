import base64
import json
from os import environ
from tweepy import Stream
from tweepy.streaming import StreamListener
from loguru import logger
import config


PUBSUB_TOPIC = environ.get('PUBSUB_TOPIC')


def publish(client, pubsub_topic, tw):
    tweet_dict = json.loads(tw)
    data = json.dumps(tweet_dict).encode("utf-8")
    encode_data = base64.b64encode(data)
    future = client.publish(pubsub_topic, encode_data)
    logger.info("Message Id {}", future.result())


class StdOutListener(StreamListener):
    """
    A listener handles tweets that are received from the stream.
    This listener dumps the tweets into a PubSub topic
    """
    client = config.get_publisher_client()

    def write_to_pubsub(self, tw):
        publish(self.client, PUBSUB_TOPIC, tw)

    def on_data(self, data):
        self.write_to_pubsub(data)

    def on_error(self, status_code):
        print(status_code)

    def on_exception(self, exception):
        print("exception", exception)
        start_stream()


def start_stream():
    stream = Stream(auth, listener)
    stream.filter(track=['FIFA', 'Euro cup 2021', 'Premier League'
                         'Say no to racism', 'Laliga', 'Bundesliga',
                         'Football Transfers', 'Lionel Messi', 'Christiano Ronaldo'
                         'Euro cup 2021 champions', 'Raheem Sterling'])


if __name__ == '__main__':
    listener = StdOutListener()
    auth = config.get_auth()
    start_stream()
