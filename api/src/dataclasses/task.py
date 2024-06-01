from dataclasses import dataclass
from src.dataclasses.repo import Repo


@dataclass
class Task:
    repo: Repo

    task_id: str

    languages: list[str]
