import logging
from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import DomainError, NotFoundError, ConflictError

logger = logging.getLogger("app")


def register_exception_handlers(app):
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        request_id = getattr(request.state, "request_id", None)
        logger.warning(f"not found | id={request_id} | {exc.__class__.__name__}: {exc}")
        return JSONResponse(
            status_code=404,
            content={"error": exc.__class__.__name__, "message": str(exc), "request_id": request_id},
        )

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError):
        request_id = getattr(request.state, "request_id", None)
        logger.warning(f"conflict | id={request_id} | {exc.__class__.__name__}: {exc}")
        return JSONResponse(
            status_code=409,
            content={"error": exc.__class__.__name__, "message": str(exc), "request_id": request_id},
        )


    @app.exception_handler(DomainError)
    async def domain_handler(request: Request, exc: DomainError):
        request_id = getattr(request.state, "request_id", None)
        logger.warning(f"domain | id={request_id} | {exc.__class__.__name__}: {exc}")
        return JSONResponse(
            status_code=400,
            content={"error": exc.__class__.__name__, "message": str(exc), "request_id": request_id},
        )