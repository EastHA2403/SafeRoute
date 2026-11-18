// 카카오맵 초기화 및 Polyline 렌더링
const map = new kakao.maps.Map(document.getElementById("map"), {
  center: new kakao.maps.LatLng(37.5670, 126.9790),
  level: 3,
});
let polyline = null;

function drawRoute(path) {
  if (polyline) polyline.setMap(null);
  const latlngs = path.map((p) => new kakao.maps.LatLng(p.lat, p.lon));
  polyline = new kakao.maps.Polyline({
    path: latlngs,
    strokeWeight: 6,
    strokeColor: "#0d6efd",
    strokeOpacity: 0.9,
  });
  polyline.setMap(map);

  const bounds = new kakao.maps.LatLngBounds();
  latlngs.forEach((ll) => bounds.extend(ll));
  map.setBounds(bounds);
}

