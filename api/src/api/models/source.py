import uuid
from pydantic import AnyUrl
from dataclasses import dataclass, field

from yarl import URL

import logging

logger = logging.getLogger(__name__)


def task_id() -> str:
    return str(uuid.uuid4())


@dataclass
class RepoInfo:
    language: str
    languages: dict
    ref: str
    size: float

# ssh://git@stash.delta.sbrf.ru/scm/lirt/spr-rrm-adapters.git
# ssh://git@stash.sigma.sbrf.ru:7999/orch/repo_analyzer.git


@dataclass
class Repo:
    url: str
    ref: str | None = None
    hash: str | None = None

    @property
    def host(self) -> str:
        return URL(self.url).host

    @property
    def name(self) -> str:
        return URL(self.url).path.split("/")[-1].removesuffix(".git")

    @property
    def project(self) -> str:
        return URL(self.url).path.split("/")[-2]


@dataclass(kw_only=True)
class SastTask:
    id: str = field(default_factory=task_id)
    # client: str = 'Test'
    # scanners: list[str] = None
    source: Repo

    # language: str = None
    languages: list[str] = None

    def dump(self):
        return {
            "task_id": self.id,
            "url": self.source.url,
            "ref": self.source.hash,
            # "scanners": self.scanners,
            # "language": self.language,
            "languages": self.languages,
            # "source": self.client
        }

    # def set_scanners(self, scanners: list):
    #     self.scanners = scanners

    def __str__(self):
        return f"Task {self.id}"


"""
Need to produce in topic smth like this
{
  "key": "094fd3b0-1615-45fb-9713-d91999b97a6e",
  "value": {
    "url": "ssh://git@stash.sigma.sbrf.ru:7999/orch/chart.git",
    "ref": "master",
    "languages": [
      "YAML"
    ]
  }
}
"""
