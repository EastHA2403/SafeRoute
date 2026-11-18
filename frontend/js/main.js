function parseLatLon(text) {
  const [lat, lon] = text.split(",").map((s) => parseFloat(s.trim()));
  return { lat, lon };
}

document.getElementById("route-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const result = document.getElementById("result");
  result.innerHTML = '<div class="text-muted">탐색 중...</div>';
  try {
    const origin = parseLatLon(document.getElementById("origin").value);
    const destination = parseLatLon(document.getElementById("destination").value);
    const data = await fetchSafeRoute(origin, destination);
    drawRoute(data.path);
    result.innerHTML = `<div class="alert alert-success">
      거리 ${data.total_distance_m} m · 안전 비용 ${data.total_cost} · ${data.elapsed_ms} ms</div>`;
  } catch (err) {
    result.innerHTML = `<div class="alert alert-danger"></div>`;
    result.firstChild.textContent = err.message;
  }
});

