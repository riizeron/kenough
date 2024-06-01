import logging
from typing import NoReturn

from src.dataclasses.kafka import KafkaMessage
from src.kafka.kafka_abc import KafkaProducerABC

logger = logging.getLogger(__name__)


class KafkaProducerMock(KafkaProducerABC):

    def __init__(self):
        self.running = True

    def send(self, kafka_message: KafkaMessage) -> NoReturn:
        """"""
