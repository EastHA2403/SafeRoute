import networkx as nx
from fastapi import APIRouter, Depends

from app.state import get_graph

router = APIRouter()


@router.get("/health", summary="서버 상태 및 그래프 적재 현황")
def health(graph: nx.Graph = Depends(get_graph)):
    return {
        "status": "ok",
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
    }

