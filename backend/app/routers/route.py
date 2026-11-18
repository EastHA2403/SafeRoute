"""요청/응답 변환만 담당. 비즈니스 로직은 services/algorithms에 위임한다."""
import networkx as nx
from fastapi import APIRouter, Depends

from app.schemas.route import RouteRequest, RouteResponse
from app.services.route_service import compute_safe_route
from app.state import get_graph

router = APIRouter()


@router.post(
    "/safe",
    response_model=RouteResponse,
    summary="안전 경로 탐색",
    responses={
        400: {"description": "잘못된 좌표/요청 형식"},
        404: {"description": "근처 노드 없음 또는 연결된 경로 없음"},
    },
)
def get_safe_route(body: RouteRequest, graph: nx.Graph = Depends(get_graph)):
    return compute_safe_route(
        graph,
        (body.origin.lat, body.origin.lon),
        (body.destination.lat, body.destination.lon),
    )

