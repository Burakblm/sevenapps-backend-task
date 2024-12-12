import json
import logging
import time

from config import settings
from kafka import KafkaConsumer
from kafka.errors import KafkaConnectionError, KafkaError, KafkaTimeoutError

logger = logging.getLogger(__name__)


def create_kafka_consumer():
    try:
        consumer = KafkaConsumer(
            settings.KAFKA_TOPIC,
            bootstrap_servers=f"{settings.KAFKA_SERVER}:{settings.KAFKA_PORT}",
            group_id="pdf_metadata_group",
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )
        logger.info("Kafka consumer created successfully.")
        return consumer
    except (KafkaTimeoutError, KafkaConnectionError, KafkaError) as e:
        logger.error(f"Kafka error: {e}")
        time.sleep(5)
        return create_kafka_consumer()
