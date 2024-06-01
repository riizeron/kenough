import logging
from typing import NoReturn

import httpx
import asyncio

from requests.auth import HTTPBasicAuth

from src.api.models.source import Repo
from src.dataclasses.creds import BBCred
from src.exceptions.git import RepoCloneException
from src.git.git_client import GitClient
from src.utils.retry import retry

from src.exceptions.api import (
    RepositoryAccessDeniedException,
    RepositoryNetworkException,
    RefNotFoundException,
    RepositoryNotFoundException
)

logger = logging.getLogger(__name__)


class GitHttpClient(GitClient):
    """"""

    def __init__(self, bb_tokens: dict[str, BBCred]):
        """"""

        self.bb_tokens = bb_tokens
        self.session = httpx.AsyncClient(verify=False)
        self.loop = asyncio.get_event_loop()

    def checkout(self, repo: Repo, output: str) -> NoReturn:
        raise NotImplementedError

    async def resolve_ref(self, repo: Repo) -> str | None:
        """"""

        url = f'https://{repo.host}/rest/api/latest/projects/{repo.project}/repos/{repo.name}/commits'
        auth = httpx.BasicAuth(
            self.bb_tokens[repo.host.removesuffix(".sbrf.ru")].username,
            self.bb_tokens[repo.host.removesuffix(".sbrf.ru")].token
        )

        params = {
            'until': repo.ref,
            'limit': 0
        }
        try:
            resp = await self.session.get(url, params=params, auth=auth)
            resp.raise_for_status()
            return resp.json()["values"][0]["id"]

        except httpx.HTTPStatusError as e:
            code = e.response.status_code
            logger.error(f"BB HTTP ERROR {code}: {e.response.json()}")
            exception_name = e.response.json()['errors'][0]['exceptionName']

            if code == 404:
                if 'NoSuchCommitException' in exception_name:
                    raise RefNotFoundException(repo.url, repo.ref) from e
                elif 'NoSuchRepositoryException' in exception_name:
                    raise RepositoryNotFoundException(repo.url) from e

            elif code == 401:
                raise RepositoryAccessDeniedException(repo.url) from e

            raise Exception(f"UNKNWON BB CODE: {code}") from e
        except Exception as e:
            logger.error(e)
            raise RepositoryNetworkException(repo.url) from e

    async def close(self):
        # httpx.AsyncClient.aclose must be awaited!
        await self.session.aclose()

    def __del__(self):
        """
        A destructor is provided to ensure that the client and the event loop are closed at exit.
        """
        # Use the loop to call async close, then stop/close loop.
        self.loop.run_until_complete(self.close())
        self.loop.close()

    # @retry(5)
    # def get_hash(
    #         self,
    #         repo: Repo,
    #         verify: bool = False,
    # ) -> str:
    #     """"""
    #
    #     url = f"https://{repo.url}/rest/api/latest/projects/{repo.project}/repos/{repo.repo}/commits"
    #     logger.info(f"Start downloading sources from {url}")
    #
    #     params = {"until": repo.ref, "limit": 0}
    #
    #     resp = self.session.get(
    #         url,
    #         auth=HTTPBasicAuth(
    #             self.bb_tokens[repo.url.removesuffix(".sbrf.ru")].username,
    #             self.bb_tokens[repo.url.removesuffix(".sbrf.ru")].token
    #         ),
    #         params=params,
    #         verify=verify
    #     )
    #     resp.raise_for_status()
    #
    #     return resp.json()["values"][0]["id"]
