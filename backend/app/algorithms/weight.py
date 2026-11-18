"""엣지 가중치(안전 비용) 계산. 순수 함수 - 단위 테스트 용이."""

SLOPE_PENALTY_PER_PCT = 0.10    # 경사 1%당 거리 대비 10% 페널티
ACCIDENT_PENALTY_PER_CASE = 0.50  # 사고 1건당 거리 대비 50% 페널티


def safe_cost(length_m: float, slope_pct: float, accident_count: float) -> float:
    """안전 비용 = 거리 x (1 + 경사 페널티 + 사고 페널티).

    TODO: 도로 파손 데이터 확보 시 항 추가. 계수는 config로 이관 검토.
    """
    penalty = (
        SLOPE_PENALTY_PER_PCT * abs(slope_pct)
        + ACCIDENT_PENALTY_PER_CASE * accident_count
    )
    return length_m * (1.0 + penalty)

