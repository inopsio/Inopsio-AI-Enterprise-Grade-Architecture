/**
 * Inopsio AI Enterprise - API Client
 * The "Nervous System" bridge between Next.js and FastAPI.
 * Handles Auth headers, Request IDs, and Error mapping automatically.
 */
import { env } from "@/env";

// Token storage key - consistent across the app
const TOKEN_KEY = "inopsio_token";

/**
 * Get the stored auth token
 */
export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

/**
 * Store the auth token
 */
export function setToken(token: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(TOKEN_KEY, token);
  // Also set as cookie for middleware access
  document.cookie = `${TOKEN_KEY}=${token}; path=/; max-age=${60 * 60 * 24 * 7}; SameSite=Lax`;
}

/**
 * Clear the auth token (logout)
 */
export function clearToken(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(TOKEN_KEY);
  document.cookie = `${TOKEN_KEY}=; path=/; max-age=0`;
}

/**
 * API Error with structured details
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public detail?: string,
    public requestId?: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Core fetch wrapper with enterprise features:
 * - Automatic JWT injection
 * - X-Request-ID for distributed tracing
 * - Structured error handling
 */
async function apiFetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();

  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);

  // Observability: Add request ID for tracing
  const requestId = crypto.randomUUID();
  headers.set("X-Request-ID", requestId);

  const response = await fetch(`${env.NEXT_PUBLIC_API_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: "include", // Important for CORS with cookies
  });

  // Extract response request ID (backend may have modified it)
  const responseRequestId = response.headers.get("X-Request-ID") || requestId;

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new ApiError(
      errorData.detail || `Request failed with status ${response.status}`,
      response.status,
      errorData.detail,
      responseRequestId
    );
  }

  // Handle empty responses (204 No Content)
  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

/**
 * Typed API client for enterprise use
 */
export const api = {
  get: <T>(url: string) => apiFetch<T>(url, { method: "GET" }),
  post: <T>(url: string, data?: unknown) =>
    apiFetch<T>(url, { method: "POST", body: data ? JSON.stringify(data) : undefined }),
  put: <T>(url: string, data: unknown) =>
    apiFetch<T>(url, { method: "PUT", body: JSON.stringify(data) }),
  patch: <T>(url: string, data: unknown) =>
    apiFetch<T>(url, { method: "PATCH", body: JSON.stringify(data) }),
  delete: <T>(url: string) => apiFetch<T>(url, { method: "DELETE" }),
};
