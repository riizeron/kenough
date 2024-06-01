from src.db.abc.repository import Repository

from service_schemas.client import Client
from service_schemas.task_sast import TaskSAST

from typing import NoReturn


class SASTRepository(Repository):
    async def get_task(self, task_id: str, client_id: int) -> TaskSAST:
        """"""

        return await self.db_client.get_task(task_id, client_id)

    async def create_task(self, task_id: str, client_id: int) -> NoReturn:
        """"""

        return await self.db_client.create_task(task_id, client_id)

    async def update_status(self, status: int, task: TaskSAST) -> NoReturn:
        """"""

        await self.db_client.update_status(status, task)

    async def send_report(self, report: dict, task: TaskSAST) -> NoReturn:
        """"""

        await self.db_client.send_report(report, task)

    async def get_client(self, cn: str) -> Client:
        """"""

        return await self.db_client.get_client(cn)

    async def create_client(self, cn: str) -> Client:
        """"""

        return await self.db_client.create_client(cn)
