# SafeRoute PM

퍼스널 모빌리티(전동 킥보드/자전거) 특화 안전 경로 추천 웹 서비스.
경사도와 사고 다발 구역을 가중치로 반영한 안전 최우선 경로를 제공합니다.

## 실행

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload      # http://localhost:8000/docs
pytest                             # 테스트
```

프론트엔드: `frontend/index.html`을 Live Server(포트 5500)로 열기.
`index.html`의 `YOUR_APP_KEY`를 카카오 JavaScript 키로 교체해야 합니다.

## 구조

- `backend/app/routers` : 요청/응답 처리 (향후 Spring Boot 이관 대상)
- `backend/app/algorithms` : 순수 경로 알고리즘 (FastAPI 비의존, 향후 마이크로서비스화)
- `backend/data/processed` : 현재는 샘플 데이터(3x3 격자). 실데이터로 교체 예정.

