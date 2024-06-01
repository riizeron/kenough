from fastapi import Request
from fastapi.responses import JSONResponse
import logging

from src.exceptions.api import (
    ArtifactAccessDeniedException,
    ArtifactNetworkException,
    ArtifactNotFoundException
)


logger = logging.getLogger(__name__)


async def artifact_not_found_exception_handler(request: Request, exc: ArtifactNotFoundException):
    logger.error(f"{exc} | CAUSE: {exc.__cause__}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "details": str(exc)
        }
    )


async def artifact_access_denied_exception_handler(request: Request, exc: ArtifactAccessDeniedException):
    logger.error(f"{exc} | CAUSE: {exc.__cause__}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "details": str(exc)
        }
    )


async def artifact_network_exception_handler(request: Request, exc: ArtifactNetworkException):
    logger.error(f"{exc} | CAUSE: {exc.__cause__}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "details": str(exc)
        }
    )