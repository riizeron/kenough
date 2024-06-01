from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

async def not_implemented_exception_handler(req: Request, exc: NotImplementedError):
    logger.error("Not implemented yet")
    return JSONResponse(
        status_code=501,
        content={
            "details": "Not implemented yet"
        }
    )