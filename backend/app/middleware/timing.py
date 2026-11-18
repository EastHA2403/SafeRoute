import logging
import time

from fastapi import Request

logger = logging.getLogger("saferoute.latency")


async def latency_logging_middleware(request: Request, call_next):
    """모든 요청의 처리 시간(Latency)을 로깅하고 응답 헤더에 노출한다."""
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-ms"] = f"{elapsed_ms:.2f}"
    logger.info(
        "%s %s -> %d | %.2fms",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response

