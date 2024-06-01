from dataclasses import dataclass


@dataclass
class KafkaConfig:
    """"""

    bootstrap_servers: str
    topic: str
    retries: str
