
from fastapi import (
    FastAPI
)
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import get_v1_router

import src.api.errors as exception_handlers

# from src.api.middleware.rate_limit import RateLimit

from src.exceptions.api import (
    ModelValidationException,
    LaunchTaskException,
    AnalyzerException,
    ArtifactNetworkException,
    ArtifactNotFoundException,
    ArtifactAccessDeniedException,
)

def get_func_app() -> FastAPI:
    
    app_func = FastAPI(
        title=          "SS API",
        description=    "API for SS",
        version=        "1.0.0"
    )

    # Middleware для CORS
    app_func.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app_func.add_middleware(RateLimit, 
    #                         requests_per_minute=config.requests_per_minute, 
    #                         request_window_size=timedelta(minutes=config.requests_window_minutes))

    # Auxiliary
    app_func.add_exception_handler(Exception, exception_handlers.exception_handler)
    app_func.add_exception_handler(NotImplementedError, exception_handlers.not_implemented_exception_handler)

    # Artifact
    app_func.add_exception_handler(ArtifactNotFoundException, exception_handlers.artifact_not_found_exception_handler)
    app_func.add_exception_handler(ArtifactAccessDeniedException, exception_handlers.artifact_access_denied_exception_handler)
    app_func.add_exception_handler(ArtifactNetworkException, exception_handlers.artifact_network_exception_handler)

    # Scanners
    # app_func.add_exception_handler(ScannersException, exception_handlers.scanners_exception_handler)

    # # Validation
    app_func.add_exception_handler(LaunchTaskException, exception_handlers.launch_task_exception_handler)
    app_func.add_exception_handler(ModelValidationException, exception_handlers.model_validation_exception_handler)
    # app_func.add_exception_handler(WrongClient, exception_handlers.wrong_client_exception_handler)

    # # Analyzers
    app_func.add_exception_handler(AnalyzerException, exception_handlers.analyzer_exception_handler)

    app_func.include_router(get_v1_router())

    return app_func