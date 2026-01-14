import logging
import uuid
from fastapi import Request

logger = logging.getLogger("app")


def register_middleware(app):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id

        logger.info(f"request start | id={request_id} | {request.method} {request.url.path}")

        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                f"request error | id={request_id} | {request.method} {request.url.path}"
            )
            raise

        response.headers["X-Request-ID"] = request_id
        logger.info(
            f"request end | id={request_id} | {request.method} {request.url.path} -> {response.status_code}"
        )
        return response