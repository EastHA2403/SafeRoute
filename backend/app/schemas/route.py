"""API 계약(요청/응답 모델). Spring Boot 이관 시 DTO 설계의 기준이 된다."""
from pydantic import BaseModel, Field


class Coordinate(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="위도", examples=[37.5665])
    lon: float = Field(..., ge=-180, le=180, description="경도", examples=[126.9780])


class RouteRequest(BaseModel):
    origin: Coordinate
    destination: Coordinate


class RouteResponse(BaseModel):
    path: list[Coordinate] = Field(..., description="폴리라인으로 그릴 좌표 배열")
    total_distance_m: float
    total_cost: float = Field(..., description="경사/사고 가중치가 반영된 안전 비용")
    node_count: int
    elapsed_ms: float = Field(..., description="경로 탐색 연산 시간(ms)")

