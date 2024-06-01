from abc import ABC

from src.db.abc.db_client import DBClient


from service_schemas.task_sast import TaskSAST
from service_schemas.client import Client

from typing import NoReturn


class Repository(ABC):
    """"""

    def __init__(self, db_client: DBClient):
        """"""

        self.db_client = db_client

    async def get_task(self, task_id: str, client_id: int) -> TaskSAST:
        """"""

    async def create_task(self, task_id: str, client_id: int) -> NoReturn:
        """"""

    async def update_status(self, status: int, task: TaskSAST) -> NoReturn:
        """"""

    async def send_report(self, report: dict, task: TaskSAST) -> NoReturn:
        """"""

    async def get_client(self, cn: str) -> Client:
        """"""

    async def create_client(self, cn: str) -> Client:
        """"""
