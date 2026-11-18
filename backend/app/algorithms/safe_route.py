"""안전 경로 탐색 (Dijkstra). FastAPI 의존성 없음."""
from dataclasses import dataclass

import networkx as nx

from app.algorithms.errors import NoPathError, NodeNotFoundError


@dataclass(frozen=True)
class RouteResult:
    path_nodes: list
    distance_m: float
    total_cost: float


def find_safe_route(graph: nx.Graph, origin: int, destination: int) -> RouteResult:
    for n in (origin, destination):
        if n not in graph:
            raise NodeNotFoundError(f"그래프에 존재하지 않는 노드입니다: {n}")
    try:
        nodes = nx.dijkstra_path(graph, origin, destination, weight="safe_cost")
    except nx.NetworkXNoPath as exc:
        raise NoPathError(f"노드 {origin} 와 {destination} 사이에 연결된 경로가 없습니다.") from exc

    pairs = list(zip(nodes, nodes[1:]))
    distance = sum(graph[u][v]["length_m"] for u, v in pairs)
    cost = sum(graph[u][v]["safe_cost"] for u, v in pairs)
    return RouteResult(path_nodes=nodes, distance_m=distance, total_cost=cost)

