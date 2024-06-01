from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from prometheus_fastapi_instrumentator import Instrumentator, metrics
from src.metrics.cust_metrics import http_requested_practies, http_codes

import logging

logger = logging.getLogger(__name__)


def get_serv_app(app_func: FastAPI) -> FastAPI:
    app_serv = FastAPI(
        title="Probs API", description="Probs API for ss-tool", version="1.0.0"
    )

    app_serv.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app_serv.get("/healthz", include_in_schema=False)
    async def return_ok_status():
        return JSONResponse(content={"message": "I'm alive"}, status_code=200)

    instrumentator = (
        Instrumentator(
            should_group_status_codes=False,
            excluded_handlers=["/docs"],
            body_handlers=[r".*"],
        )
        .instrument(app_func)
        .expose(app_serv)
    )

    # metrics.Info(request=Request, response=Response, method="GET, POST", modified_handler=None, modified_status="200, 400, 404, 429, 500", modified_duration=None)

    instrumentator.add(http_requested_practies())
    instrumentator.add(http_codes())
    instrumentator.add(metrics.latency())
    instrumentator.add(metrics.requests())

    logger.info("Metrics enable")

    return app_serv
