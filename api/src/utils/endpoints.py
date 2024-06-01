from typing import Iterable
from fastapi import FastAPI
from starlette.routing import Mount

import logging
import tabulate

logger = logging.getLogger(__name__)

def gen_routes(app: FastAPI | Mount) -> Iterable[tuple[str, str]]:
    for route in app.routes:
        if isinstance(route, Mount):
            yield from (
                (f"{route.path}{path}", name) for path, name in gen_routes(route)
            )
        else:
            yield (
                route.path,
                "{}.{}".format(route.endpoint.__module__, route.endpoint.__qualname__),
            )

def list_routes(app: FastAPI) -> None:
    
    routes = sorted(set(gen_routes(app)))  # also readable enough
    logger.info(tabulate.tabulate(routes, headers=["path", "full name"]))
