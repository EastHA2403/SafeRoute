"""좌표 -> 최근접 도로망 노드 매핑."""
import math

import networkx as nx

from app.algorithms.errors import InvalidCoordinateError, NodeNotFoundError

EARTH_RADIUS_M = 6_371_000.0


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """두 좌표 사이의 대원 거리(m)."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = p2 - p1
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(a))


def validate_coordinate(lat: float, lon: float) -> None:
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        raise InvalidCoordinateError(f"유효하지 않은 좌표입니다: lat={lat}, lon={lon}")


def find_nearest_node(
    graph: nx.Graph, lat: float, lon: float, max_distance_m: float = 500.0
):
    """가장 가까운 노드 ID를 반환한다. max_distance_m 이내에 없으면 NodeNotFoundError.

    TODO: 노드 수가 커지면 KD-Tree/BallTree(scikit-learn)로 교체.
    """
    validate_coordinate(lat, lon)
    best_id, best_dist = None, float("inf")
    for node_id, data in graph.nodes(data=True):
        d = haversine_m(lat, lon, data["lat"], data["lon"])
        if d < best_dist:
            best_id, best_dist = node_id, d
    if best_id is None or best_dist > max_distance_m:
        raise NodeNotFoundError(
            f"({lat}, {lon}) 반경 {max_distance_m:.0f}m 내에 도로망 노드가 없습니다."
        )
    return best_id

