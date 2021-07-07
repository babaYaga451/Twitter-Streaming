from loguru import logger
import base64
from utils import message_helper


def handle_request(event, context):
    logger.info("MessageId {} Timestamp : {}",
                context.event_id, context.timestamp)

    if 'data' in event:
        message = base64.b64decode(event['data']).decode('utf-8')  # Decoding messages received from PubSub
        message_helper.process_message(message, context.timestamp, context.event_id)
