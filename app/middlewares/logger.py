import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger(__name__)

        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time
        client_ip = request.client.host
        method = request.method
        url = request.url.path
        status_code = response.status_code

        logger.info(f"{client_ip} - {method} {url} - {status_code} - {duration:.2f}s")

        return response
