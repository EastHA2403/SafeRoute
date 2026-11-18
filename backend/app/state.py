"""인메모리 상태 접근용 의존성. 테스트에서는 dependency_overrides로 교체 가능."""
import networkx as nx
from fastapi import HTTPException, Request


def get_graph(request: Request) -> nx.Graph:
    graph = getattr(request.app.state, "graph", None)
    if graph is None:
        raise HTTPException(status_code=503, detail="도로망 그래프가 아직 로드되지 않았습니다.")
    return graph

