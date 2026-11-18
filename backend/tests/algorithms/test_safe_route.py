"""알고리즘 단위 테스트 - FastAPI 없이 순수하게 실행된다."""
import pytest

from app.algorithms.errors import InvalidCoordinateError, NoPathError, NodeNotFoundError
from app.algorithms.graph_loader import load_road_graph
from app.algorithms.nearest_node import find_nearest_node
from app.algorithms.safe_route import find_safe_route
from app.core.config import settings


@pytest.fixture(scope="module")
def graph():
    return load_road_graph(settings.NODES_CSV, settings.EDGES_CSV, settings.ACCIDENTS_CSV)


def test_graph_loaded(graph):
    assert graph.number_of_nodes() == 9
    assert graph.number_of_edges() == 12


def test_safe_route_avoids_steep_accident_center(graph):
    # 1 -> 9 : 중앙(노드 5, 급경사+사고)을 피해 외곽으로 우회해야 한다.
    result = find_safe_route(graph, 1, 9)
    assert 5 not in result.path_nodes
    assert result.path_nodes[0] == 1 and result.path_nodes[-1] == 9


def test_nearest_node(graph):
    assert find_nearest_node(graph, 37.56601, 126.97801) == 1


def test_invalid_coordinate(graph):
    with pytest.raises(InvalidCoordinateError):
        find_nearest_node(graph, 100.0, 126.0)


def test_far_coordinate_not_found(graph):
    with pytest.raises(NodeNotFoundError):
        find_nearest_node(graph, 35.0, 129.0)


def test_isolated_node_no_path(graph):
    g = graph.copy()
    g.add_node(99, lat=37.6, lon=127.0, accidents=0.0)
    with pytest.raises(NoPathError):
        find_safe_route(g, 1, 99)

