from src.db.abc.db_client import DBClient

from sqlalchemy import select

from src.utils.retry import retry

from service_schemas.task_sast import TaskSAST


class PostgresClient(DBClient):
    """"""

    @retry(max_retries=5, timeout=0.01)
    async def get_task(self, task_id: str) -> TaskSAST:
        """"""

        async with self.connector.get_session() as session:
            task = await session.execute(select(TaskSAST).where(
                TaskSAST.taskId == task_id,
            ))

        first = task.first()

        return first[0] if first else None

    @retry(max_retries=5, timeout=0.01)
    async def create_task(self, task_id: str) -> TaskSAST:
        """"""

        task = TaskSAST(taskId=task_id, status=1)

        async with self.connector.get_session() as session:
            session.add(task)
            await session.commit()

        return task

    @retry(max_retries=5, timeout=0.01)
    async def update_status(self, status: int, task: TaskSAST) -> None:
        """"""

        async with self.connector.get_session() as session:
            task.status = status
            session.add(task)
            await session.commit()

    @retry(max_retries=5, timeout=0.01)
    async def send_report(self, report: dict, task: TaskSAST) -> None:
        """"""

        async with self.connector.get_session() as session:
            task.status = 3
            task.result = report
            session.add(task)
            await session.commit()
