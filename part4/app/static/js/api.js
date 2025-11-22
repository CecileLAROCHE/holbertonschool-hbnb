export const API_BASE_URL = "http://127.0.0.1:5000/api/v1";

// FETCH WRAPPER
export async function apiGet(endpoint, headers = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, { headers });
    if (!response.ok) throw new Error("API GET error");
    return response.json();
}

export async function apiPost(endpoint, body, headers = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...headers },
        body: JSON.stringify(body)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "API POST error");
    return data;
}

export async function apiDelete(endpoint, headers = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "DELETE",
        headers
    });
    if (!response.ok) throw new Error("API DELETE error");
    return {};
}
