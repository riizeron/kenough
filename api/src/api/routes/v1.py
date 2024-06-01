from fastapi.encoders import jsonable_encoder
import logging
from typing import Optional, Annotated
from enum import Enum

from fastapi import APIRouter, Header, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.api.core.launch_source import LaunchSourceService
from src.api.models.repo_validated import RepoValidated
from src.api.models.source import (
    SastTask,
    Repo
)

from src.git.git_http import GitHttpClient


# dependencies
from src.db import sast_repository as sast_repository_dependencies
from src.db.abc.repository import Repository
from src.git import git_http_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1")


class TaskStatus(Enum):
    CREATED = 0
    STARTED = 1
    FAILED = 2
    FINISHED = 3

    def __str__(self):
        return self.name.split(".")[-1]


def get_git_http_client() -> GitHttpClient:
    return git_http_client

def get_repository() -> Repository:
    return sast_repository_dependencies


def get_launch_source_service() -> LaunchSourceService:
    return LaunchSourceService(scm=get_git_http_client())


repository_dependencies = Annotated[Repository, Depends(get_repository)]
launch_source_service_dependencies = Annotated[LaunchSourceService, Depends(get_launch_source_service)]


@router.post("/launch")
async def sast_launch(
        repo_model: RepoValidated,
        launch_service: launch_source_service_dependencies,
        repository: repository_dependencies,
):
    """"""

    repo = Repo(url=str(repo_model.url), ref=repo_model.ref)

    task = SastTask(source=repo)

    logger.info(f"{task} | GET")

    task_id = await launch_service(task)

    logger.info(f"{task} | LAUNCHED. Details: {task.dump()}")

    await repository.create_task(task_id)

    return JSONResponse(status_code=201, content=jsonable_encoder({"taskId": task_id}))


@router.get("/get_report", tags=["Report"])
async def get_report(
        task_id: str,
        repository: repository_dependencies,
):
    
    task = await repository.get_task(task_id)
    if not task:
        return JSONResponse(
            status_code=404, content=jsonable_encoder({"status": "NotFound", "report": ""})
        )

    responses = {
        TaskStatus.CREATED: JSONResponse(
            status_code=200, content=jsonable_encoder({"status": "Created", "report": ""})),
        TaskStatus.STARTED: JSONResponse(
            status_code=200, content=jsonable_encoder({"status": "Started", "report": ""})),
        TaskStatus.FAILED: JSONResponse(
            status_code=200, content=jsonable_encoder({"status": "Failed", "report": ""})),
        TaskStatus.FINISHED: JSONResponse(
            status_code=200, content=jsonable_encoder({"status": "Finished", "report": task.result})),
    }

    return responses[TaskStatus(task.status)]
