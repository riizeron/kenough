from fastapi import Request
from fastapi.responses import JSONResponse
import logging

from src.exceptions.api import AnalyzerException

logger = logging.getLogger('orch.api.' + __name__)


async def analyzer_exception_handler(request: Request, exc: AnalyzerException):
    logger.exception(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "details": str(exc)
        }
    )