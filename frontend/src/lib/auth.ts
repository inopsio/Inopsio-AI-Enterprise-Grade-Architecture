/**
 * Inopsio AI Enterprise - Auth Service
 * Handles login, logout, and session management.
 */
import { api, setToken, clearToken, getToken } from "./api";
import { env } from "@/env";
import type { AuthResponse, User } from "@/types/api-types";

const API_PREFIX = "/api/v1";

/**
 * Login with email and password
 * Returns the access token on success
 */
export async function login(email: string, password: string): Promise<AuthResponse> {
  // OAuth2 expects form data, not JSON
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await fetch(
    `${env.NEXT_PUBLIC_API_URL}${API_PREFIX}/auth/login`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
      credentials: "include",
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Login failed");
  }

  const data: AuthResponse = await response.json();
  setToken(data.access_token);
  return data;
}

/**
 * Get the current authenticated user
 */
export async function getCurrentUser(): Promise<User> {
  return api.get<User>(`${API_PREFIX}/auth/test-token`);
}

/**
 * Logout - clear token and redirect
 */
export function logout(redirectTo = "/signin"): void {
  clearToken();
  if (typeof window !== "undefined") {
    window.location.href = redirectTo;
  }
}

/**
 * Check if user is authenticated (client-side only)
 */
export function isAuthenticated(): boolean {
  return !!getToken();
}

/**
 * Decode JWT payload (without verification - for client display only)
 */
export function decodeToken(token: string): { sub: string; exp: number } | null {
  try {
    const base64Payload = token.split(".")[1];
    const payload = atob(base64Payload);
    return JSON.parse(payload);
  } catch {
    return null;
  }
}

/**
 * Check if token is expired
 */
export function isTokenExpired(token: string): boolean {
  const payload = decodeToken(token);
  if (!payload) return true;
  // Add 60 second leeway for clock skew (as per audit report)
  return Date.now() >= (payload.exp * 1000) - 60000;
}
