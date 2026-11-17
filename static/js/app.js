// static/js/app.js
// Shared helpers used by every page.

// Colour for each risk level (matches the labels from risk_service.py).
const COLORS = {
  CRIT: "#a7433d",
  HIGH: "#b86b36",
  MED:  "#987a31",
  LOW:  "#477a58",
};

// Returns a small coloured label, e.g. badge("CRIT") -> red "CRIT" tag.
function badge(level) {
  const color = COLORS[level] || COLORS.LOW;
  return `<span class="risk-badge" style="--badge-color:${color}">${level}</span>`;
}

// Calls one of our API routes and returns the JSON reply.
// Usage: await api("/api/forests")
//        await api("/api/incidents", "POST", { lat: -0.58, lon: 35.55 })
async function api(url, method = "GET", body) {
  const response = await fetch(url, {
    method: method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const result = await response.json();
  if (!response.ok) {
    const error = new Error(result.error || `Request failed (${response.status})`);
    error.status = response.status;
    throw error;
  }
  return result;
}

// Creates a Leaflet map inside the HTML element with the given id,
// centred on Kenya, with OpenStreetMap tiles.
function makeMap(elementId) {
  const map = L.map(elementId).setView([-1.3, 37.5], 6);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap",
  }).addTo(map);
  return map;
}
