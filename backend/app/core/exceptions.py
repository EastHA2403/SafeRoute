"""도메인 예외 -> HTTP 응답 매핑. 에러 포맷: {"error": {"code", "message"}}"""
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.algorithms.errors import (
    InvalidCoordinateError,
    NoPathError,
    NodeNotFoundError,
    RouteError,
)

logger = logging.getLogger("saferoute.error")

_STATUS_MAP: dict[type[RouteError], tuple[int, str]] = {
    InvalidCoordinateError: (400, "INVALID_COORDINATE"),
    NodeNotFoundError: (404, "NODE_NOT_FOUND"),
    NoPathError: (404, "NO_PATH"),
}


def _body(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RouteError)
    async def route_error_handler(request: Request, exc: RouteError):
        status, code = _STATUS_MAP.get(type(exc), (400, "ROUTE_ERROR"))
        return JSONResponse(status_code=status, content=_body(code, str(exc)))

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        # 위도/경도 범위 위반 등 입력 오류는 400으로 통일
        return JSONResponse(
            status_code=400,
            content=_body("INVALID_REQUEST", "요청 형식 또는 좌표 값이 올바르지 않습니다.")
            | {"detail": jsonable(exc.errors())},
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception):
        logger.exception("처리되지 않은 예외: %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content=_body("INTERNAL_ERROR", "서버 내부 오류가 발생했습니다."),
        )


def jsonable(errors: list[dict]) -> list[dict]:
    """pydantic 에러 중 직렬화 불가능한 필드(ctx 등) 제거."""
    return [{"loc": e.get("loc"), "msg": e.get("msg"), "type": e.get("type")} for e in errors]

