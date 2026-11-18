"""라우터와 알고리즘 사이의 오케스트레이션 계층."""
import logging
import time

import networkx as nx

from app.algorithms.nearest_node import find_nearest_node
from app.algorithms.safe_route import find_safe_route

logger = logging.getLogger("saferoute.service")


def compute_safe_route(
    graph: nx.Graph, origin: tuple[float, float], destination: tuple[float, float]
) -> dict:
    """(lat, lon) 두 쌍을 받아 경로 딕셔너리를 반환한다. HTTP/Pydantic 비의존."""
    t0 = time.perf_counter()
    origin_node = find_nearest_node(graph, *origin)
    dest_node = find_nearest_node(graph, *destination)
    result = find_safe_route(graph, origin_node, dest_node)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    path = [
        {"lat": graph.nodes[n]["lat"], "lon": graph.nodes[n]["lon"]}
        for n in result.path_nodes
    ]
    logger.info(
        "경로 탐색 완료 | %s -> %s | nodes=%d | dist=%.0fm | %.2fms",
        origin_node, dest_node, len(path), result.distance_m, elapsed_ms,
    )
    return {
        "path": path,
        "total_distance_m": round(result.distance_m, 2),
        "total_cost": round(result.total_cost, 2),
        "node_count": len(path),
        "elapsed_ms": round(elapsed_ms, 3),
    }

