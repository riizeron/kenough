import logging
import json

from src.git.git_client import GitClient
from src.kafka.kafka_abc import KafkaProducerABC

from src.api.models.source import SastTask

from src.dataclasses.kafka import KafkaMessage

logger = logging.getLogger(__name__)


class LaunchSourceService:

    def __init__(self, producer: KafkaProducerABC, scm: GitClient):
        self.producer = producer
        self.scm = scm

    async def __call__(self, task: SastTask) -> str:

        task.source.commit_hash = await self.scm.resolve_ref(task.source)
        logger.info(f"{task} | REPO ACCESSED | {task.source}")

        languages = ["YAML"]
        task.languages = languages

        self.producer.send(KafkaMessage(value=json.dumps(task.dump()), key=task.id))

        logger.info(f"{task} | TASK SENT")

        return task.id