# API 명세 (요약)

상세 명세는 서버 실행 후 `/docs` (Swagger) 또는 `/redoc` 참고.

## POST /api/v1/routes/safe

요청
```json
{ "origin": {"lat": 37.5660, "lon": 126.9780}, "destination": {"lat": 37.5680, "lon": 126.9800} }
```

응답 200
```json
{ "path": [{"lat": 37.566, "lon": 126.978}], "total_distance_m": 0, "total_cost": 0, "node_count": 0, "elapsed_ms": 0 }
```

에러 포맷: `{"error": {"code": "...", "message": "..."}}`

| 상태 | code | 상황 |
|---|---|---|
| 400 | INVALID_REQUEST / INVALID_COORDINATE | 좌표 범위·형식 오류 |
| 404 | NODE_NOT_FOUND | 좌표 반경 내 도로망 노드 없음 |
| 404 | NO_PATH | 고립 노드 등 연결된 경로 없음 |
| 500 | INTERNAL_ERROR | 서버 내부 오류 |

