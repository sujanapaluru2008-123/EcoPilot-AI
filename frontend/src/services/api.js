
const API_BASE_URL = "http://127.0.0.1:8000";

async function fetchJSON(url) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}


// Get all campus buildings
export async function getBuildings() {
  return fetchJSON(`${API_BASE_URL}/buildings`);
}


// Get dashboard data for one building
export async function getDashboard(building) {
  return fetchJSON(
    `${API_BASE_URL}/dashboard/${encodeURIComponent(building)}`
  );
}


// Get historical data for one building
export async function getHistory(building) {
  return fetchJSON(
    `${API_BASE_URL}/history/${encodeURIComponent(building)}`
  );
}