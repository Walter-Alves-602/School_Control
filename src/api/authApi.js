const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function login(username, password) {
  const body = new URLSearchParams({ username, password });

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || "Não foi possível fazer login.");
  }

  return data.access_token;
}
