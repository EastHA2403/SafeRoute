// 백엔드 호출 전담. 서버 주소는 여기서만 관리한다.
const API_BASE = "http://localhost:8000/api/v1";

async function fetchSafeRoute(origin, destination) {
  const res = await fetch(`${API_BASE}/routes/safe`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ origin, destination }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data?.error?.message ?? "요청에 실패했습니다.");
  return data;
}

