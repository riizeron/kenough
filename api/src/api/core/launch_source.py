import logging

from src.git.git_client import GitClient
from src.kube.client import KubeClient

from src.api.models.source import SastTask
from src.jinja.templator import Templator


logger = logging.getLogger(__name__)


class LaunchSourceService:

    def __init__(self, kube: KubeClient, scm: GitClient, templator: Templator):
        self.scm = scm
        self.kube_client = kube
        self.templator = templator

    async def __call__(self, task: SastTask) -> str:

        task.source.commit_hash = await self.scm.resolve_ref(task.source)
        logger.info(f"{task} | REPO ACCESSED | {task.source}")

        job = self.templator.render(task_id=task.id, task_config=task)

        self.kube_client.create_from_dict(job)

        logger.info(f"{task} | TASK LAUNCHED")

        return task.id