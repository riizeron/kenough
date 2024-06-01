from dataclasses import dataclass


@dataclass
class KafkaMessage:

    value: str
    key: str
