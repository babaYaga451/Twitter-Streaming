import json
from os import environ
from dotenv import load_dotenv
from tweepy import Stream
from tweepy.streaming import StreamListener

import config

load_dotenv()

PUBSUB_TOPIC = environ.get('PUBSUB_TOPIC')


def callback(future):
    try:
        message_id = future.result()
        print(message_id)
    except BaseException as e:
        print(e)


def publish(client, pubsub_topic, tw):
    data = json.dumps(tw).encode("utf-8")
    future = client.publish(pubsub_topic, data)
    future.add_done_callback(callback)


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
    stream.filter(track=['Avengers', 'Loki', 'Tomorrow War'])


if __name__ == '__main__':
    listener = StdOutListener()
    auth = config.get_auth()
    start_stream()
