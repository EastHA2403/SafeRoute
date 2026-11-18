"""알고리즘 계층의 도메인 예외.

FastAPI/HTTP에 의존하지 않는다. (MSA 분리 시 그대로 가져갈 수 있도록)
HTTP 상태 코드 매핑은 app/core/exceptions.py 에서 수행한다.
"""


class RouteError(Exception):
    """모든 경로 탐색 도메인 예외의 베이스."""


class InvalidCoordinateError(RouteError):
    """위도/경도 범위가 잘못된 경우 (-> 400)."""


class NodeNotFoundError(RouteError):
    """좌표 근처에서 도로망 노드를 찾지 못한 경우 (-> 404)."""


class NoPathError(RouteError):
    """두 노드 사이에 연결된 경로가 없는 경우 - 고립 노드 등 (-> 404)."""

