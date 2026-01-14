/**
 * Inopsio AI Enterprise - Core API Types
 * TypeScript mirrors of FastAPI Pydantic models.
 * 
 * This file contains ONLY the generic multi-tenant foundation.
 * Add your SaaS-specific types when you clone this template.
 *
 * @see backend/app/schemas/*.py for source of truth
 */

// ============================================
// AUTH TYPES (mirrors schemas/token.py)
// ============================================

export interface AuthResponse {
  access_token: string;
  token_type: "bearer";
}

export interface TokenPayload {
  sub: string; // user_id
  exp: number; // expiration timestamp
}

// ============================================
// USER TYPES (mirrors schemas/user.py)
// ============================================

export interface User {
  id: string;
  email: string;
  fullName: string | null;
  isActive: boolean;
  createdAt: string; // ISO 8601
}

export interface UserCreate {
  email: string;
  password: string;
  fullName?: string;
}

export interface UserUpdate {
  email?: string;
  fullName?: string;
  password?: string;
}

// ============================================
// ORGANIZATION TYPES (multi-tenant foundation)
// ============================================

export interface Organization {
  id: string;
  name: string;
  slug: string;
  plan: string; // Customize per SaaS: "free" | "pro" | "enterprise"
  createdAt: string;
  updatedAt: string;
}

export interface Member {
  id: string;
  role: "owner" | "admin" | "member";
  userId: string;
  organizationId: string;
}

// ============================================
// API ERROR TYPES
// ============================================

export interface ApiErrorResponse {
  detail: string;
}

// ============================================
// PAGINATION (common pattern)
// ============================================

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}
