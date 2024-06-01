from src.configs.config import kafka_config

from src.kafka.kafka_client import KafkaProducerClient


kafka_producer = KafkaProducerClient(kafka_config)
