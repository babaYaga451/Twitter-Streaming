from loguru import logger
import base64
from utils import message_helper
from repository import ElasticSearch as repository
from elasticsearch import ElasticsearchException, ImproperlyConfigured


def handle_request(event, context):
    logger.info("MessageId {} Timestamp : {}",
                context.event_id, context.timestamp)

    if 'data' in event:
        message = base64.b64decode(event['data']).decode('utf-8')  # Decoding messages received from PubSub
        logger.info("Message recieved from pubsub {}", message)
        tweet = message_helper.process_message(message, context.event_id)
        if tweet:
            try:
                repository.save(tweet)
            except ElasticsearchException as e:
                logger.error(str(e))
            except ImproperlyConfigured as e:
                logger.error(str(e))
