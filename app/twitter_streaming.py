from tweepy import OAuthHandler
from tweepy import StreamListener, Stream
from os import environ
from dotenv import load_dotenv

load_dotenv()

consumer_key = environ.get('CONSUMER_KEY')
consumer_secret = environ.get('CONSUMER_SECRET')
access_token = environ.get('ACCESS_TOKEN')
access_token_secret = environ.get('ACCESS_TOKEN_SECRET')


class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)

    def on_error(self, status_code):
        print(status_code)


if __name__ == '__main__':
    listener = StdOutListener()

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, listener)
    stream.filter(track=[
        'Euro Cup', 'Lionel Messi', 'Spain'
    ])
