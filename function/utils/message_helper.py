import json
from loguru import logger


def process_message(message, timestamp, event_id):
    logger.info("Processing messages.. event_id: {}", event_id)
    tweet = json.loads(message)
    logger.info("Message body: {}", tweet)


