from loguru import logger
import base64


def handle_request(event, context):
    logger.info("This Function was triggered by messageId {} published at {}",
                context.event_id, context.timestamp)

    if 'data' in event:
        message = base64.b64decode(event['data']).decode('utf-8')
        logger.info("Message recieved {}", message)
