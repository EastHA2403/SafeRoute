"""SafeRoute PM - FastAPI 진입점.

책임: 앱 생성, Lifespan(인메모리 데이터 적재), 미들웨어/예외 핸들러/라우터 등록.
경로 계산 로직은 algorithms/ 에 위치하며 이 파일에서는 호출만 한다.
"""
import logging
import os
import sys
import time
from contextlib import asynccontextmanager

import psutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.algorithms.graph_loader import load_road_graph
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging_config import setup_logging
from app.middleware.timing import latency_logging_middleware
from app.routers import health, route

setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger("saferoute.main")


def _rss_mb() -> float:
    """현재 프로세스의 실제 메모리 사용량(MB)."""
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """서버 기동 시 1회만 그래프를 RAM에 적재하고, 종료 시 해제한다."""
    logger.info("서버 기동: 인메모리 데이터 적재 시작")
    mem_before = _rss_mb()
    t0 = time.perf_counter()

    graph = load_road_graph(
        nodes_path=settings.NODES_CSV,
        edges_path=settings.EDGES_CSV,
        accidents_path=settings.ACCIDENTS_CSV,
    )
    app.state.graph = graph  # 의존성(app.state.get_graph)으로 접근

    elapsed = time.perf_counter() - t0
    mem_after = _rss_mb()
    logger.info(
        "그래프 적재 완료 | nodes=%d edges=%d | 소요=%.2fs | "
        "메모리 %.1fMB -> %.1fMB (+%.1fMB) | graph_obj=%dB",
        graph.number_of_nodes(),
        graph.number_of_edges(),
        elapsed,
        mem_before,
        mem_after,
        mem_after - mem_before,
        sys.getsizeof(graph),  # 얕은 크기. 정확한 값은 RSS 증가량 참고
    )

    yield  # ---- 서버 동작 구간 ----

    logger.info("서버 종료: 그래프 메모리 해제")
    app.state.graph = None


app = FastAPI(
    title="SafeRoute PM API",
    description="퍼스널 모빌리티(전동 킥보드/자전거) 특화 안전 경로 추천 API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",     # Swagger UI
    redoc_url="/redoc",   # ReDoc
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(latency_logging_middleware)

register_exception_handlers(app)  # 400/404/500 JSON 에러 포맷 통일

app.include_router(health.router, tags=["Health"])
app.include_router(route.router, prefix="/api/v1/routes", tags=["Routes"])

