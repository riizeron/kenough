from src.api.models.source import Repo
from abc import ABC, abstractmethod

from typing import NoReturn


class GitClient(ABC):

    @abstractmethod
    def checkout(self, repo: Repo, output: str) -> str:
        """"""

    @abstractmethod
    async def resolve_ref(self, repo: Repo) -> str:
        """"""
