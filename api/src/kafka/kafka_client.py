import logging

from kafka import KafkaProducer

from src.kafka.kafka_abc import KafkaProducerABC

from src.configs.kafka_config import KafkaConfig

from src.dataclasses.kafka import KafkaMessage

from typing import Iterator, NoReturn

logger = logging.getLogger(__name__)


class KafkaProducerClient(KafkaProducerABC):

    def __init__(self, kafka_config: KafkaConfig):
        logger.info(f"Sending topics: {kafka_config.topic}")
        self.topic = kafka_config.topic

        self.producer = KafkaProducer(
            client_id=kafka_config.client_id,
            bootstrap_servers=kafka_config.bootstrap_servers,
            retries=kafka_config.retries,
            max_request_size=26214400,
            compression_type="gzip",
            # auto_offset_reset=kafka_config.auto_offset_reset,
            # value_deserializer=lambda m: json.loads(m.decode()),
            # key_deserializer=bytes.decode,
        )

    def send(self, kafka_message: KafkaMessage) -> NoReturn:
        """"""

        value = kafka_message.value.encode('utf-8')
        key = kafka_message.key.encode('utf-8')

        self.producer.send(self.topic, key=key, value=value)
