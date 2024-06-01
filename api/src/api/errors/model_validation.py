from fastapi import Request
from fastapi.responses import JSONResponse
import logging

from src.exceptions.api import ModelValidationException

logger = logging.getLogger('orch.api.' + __name__)


async def model_validation_exception_handler(request: Request, exc: ModelValidationException):
    logger.error(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "details": f"{exc.message}"
        }
    )
