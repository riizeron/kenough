from abc import ABC, abstractmethod

from src.dataclasses.kafka import KafkaMessage
from typing import Iterator, NoReturn


class KafkaProducerABC(ABC):

    @abstractmethod
    def send(self, kafka_message: KafkaMessage) -> NoReturn:
        """"""
