import json
from tweepy import StreamListener, Stream
from os import environ
from dotenv import load_dotenv
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
    for tweet in tw:
        data = json.dumps(tweet).encode("utf-8")
        future = client.publish(pubsub_topic, data)
        future.add_done_callback(callback)


class StdOutListener(StreamListener):
    """
    A listener handles tweets that are received from the stream.
    This listener dumps the tweets into a PubSub topic
    """

    count = 0
    tweets = []
    batch_size = 50
    total_tweets = 250
    client = config.get_publisher_client()

    def write_to_pubsub(self, tw):
        publish(self.client, PUBSUB_TOPIC, tw)

    def on_data(self, data):
        self.tweets.append(data)
        if len(self.tweets) >= self.batch_size:
            self.write_to_pubsub(self.tweets)
            self.tweets = []
        self.count += 1
        if self.count > self.total_tweets:
            print("End of tweets")
            return False

    def on_error(self, status_code):
        print(status_code)


if __name__ == '__main__':
    listener = StdOutListener()

    auth = config.get_auth()

    stream = Stream(auth, listener)
    stream.filter(track=[
        'Avengers', 'Loki', 'Tomorrow War'
    ])
