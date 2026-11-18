"""CSV -> NetworkX 도로망 그래프 구축.

입력 스키마
- nodes.csv     : node_id, lat, lon
- edges.csv     : source, target, length_m, slope_pct
- accidents.csv : lat, lon, count
"""
from pathlib import Path

import networkx as nx
import pandas as pd

from app.algorithms.nearest_node import find_nearest_node
from app.algorithms.weight import safe_cost


def _require(path: Path) -> Path:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"데이터 파일이 없습니다: {path}")
    return path


def load_road_graph(
    nodes_path: Path, edges_path: Path, accidents_path: Path
) -> nx.Graph:
    nodes = pd.read_csv(_require(nodes_path))
    edges = pd.read_csv(_require(edges_path))
    accidents = pd.read_csv(_require(accidents_path))

    g = nx.Graph()
    for row in nodes.itertuples(index=False):
        g.add_node(int(row.node_id), lat=float(row.lat), lon=float(row.lon), accidents=0.0)

    # 사고 지점을 가장 가까운 노드에 귀속 (반경 제한 없이 매핑)
    for row in accidents.itertuples(index=False):
        node_id = find_nearest_node(g, float(row.lat), float(row.lon), max_distance_m=float("inf"))
        g.nodes[node_id]["accidents"] += float(row.count)

    for row in edges.itertuples(index=False):
        u, v = int(row.source), int(row.target)
        accident_count = (g.nodes[u]["accidents"] + g.nodes[v]["accidents"]) / 2
        g.add_edge(
            u,
            v,
            length_m=float(row.length_m),
            slope_pct=float(row.slope_pct),
            accident_count=accident_count,
            safe_cost=safe_cost(float(row.length_m), float(row.slope_pct), accident_count),
        )
    return g

