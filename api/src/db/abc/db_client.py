from src.db.abc.connector import Connector

from abc import ABC, abstractmethod

from service_schemas.client import Client
from service_schemas.task_ss import TaskSS


class DBClient(ABC):
    """"""

    def __init__(self, connector: Connector):
        """"""

        self.connector = connector

    @abstractmethod
    async def get_task(self, task_id, client_id: int) -> TaskSS:
        """"""

    @abstractmethod
    async def create_task(self, task_id: str, client_id: int) -> TaskSS:
        """"""

    @abstractmethod
    async def update_status(self, status: int, task: TaskSS) -> None:
        """"""

    @abstractmethod
    async def send_report(self, report: dict, task: TaskSS) -> None:
        """"""

    @abstractmethod
    async def get_client(self, cn: str) -> Client:
        """"""

    @abstractmethod
    async def create_client(self, cn: str) -> Client:
        """"""
