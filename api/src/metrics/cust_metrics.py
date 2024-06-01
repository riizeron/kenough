from typing import Callable
import logging
import json
from prometheus_fastapi_instrumentator.metrics import Info
from prometheus_client import Counter
# from fastapi import Request

logger = logging.getLogger(__name__)


def http_requested_practies() -> Callable[[Info], None]:
    METRIC_PRACT = Counter(
        "http_requested_practies",
        "Number of times a certain practies has been requested.",
        labelnames=("practies",),
    )

    def instrumentation(info: Info) -> None:
        # logger.info(info.response.status_code)
        try:
            pract_arr = json.loads(info.response.body.decode("utf-8"))[
                "applicable_practices"
            ]
            for pract in pract_arr:
                METRIC_PRACT.labels(pract).inc()
        except Exception:
            pass

    return instrumentation


def http_codes() -> Callable[[Info], None]:
    METRIC_PRACT = Counter(
        "http_codes", "Number of codes that api returned.", labelnames=("codes",)
    )

    def instrumentation(info: Info) -> None:
        # codes_arr=["200", "400", "404", "429", "500", "302"]
        code = info.response.status_code
        METRIC_PRACT.labels(code).inc()

    return instrumentation
