import json
from kafka import KafkaProducer as KafkaProducerClient
from app.core.config import settings


class CustomKafkaProducer:
    def __init__(self):
        """
        Initializes the Kafka producer with the Kafka server and port from the settings.
        The value serializer ensures that messages are encoded as JSON before sending.
        """
        self.producer = KafkaProducerClient(
            bootstrap_servers=f"{settings.KAFKA_SERVER}:{settings.KAFKA_PORT}",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        self.kafka_topic = settings.KAFKA_TOPIC

    def send_to_kafka(self, document_id: str):
        """
        Sends the provided document_id to Kafka as a JSON-encoded message.

        Args:
            document_id (str): The ID of the document to be sent.
        """
        message = {"document_id": document_id}
        self.producer.send(self.kafka_topic, message)
        self.producer.flush()
