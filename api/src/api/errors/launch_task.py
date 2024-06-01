from fastapi import Request
from fastapi.responses import JSONResponse
import logging

from src.exceptions.api import LaunchTaskException

logger = logging.getLogger('orch.api.' + __name__)


async def launch_task_exception_handler(request: Request, exc: LaunchTaskException):
    logger.error(exc, stack_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "details": f"{exc}"
        }
    )
