/**
 * Inopsio AI Enterprise - Route Protection Middleware
 * The "Shield" that guards protected routes.
 * Runs at the Edge before page rendering.
 */
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Token cookie name - must match lib/api.ts
const TOKEN_KEY = "inopsio_token";

// Routes that require authentication
const PROTECTED_PATTERNS = ["/dashboard", "/admin"];

// Routes that should redirect TO dashboard if already authenticated
const AUTH_ROUTES = ["/signin", "/signup", "/login"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get(TOKEN_KEY)?.value;

  // Extract locale from path (e.g., /en/dashboard -> en)
  const localeMatch = pathname.match(/^\/([a-z]{2})\//);
  const locale = localeMatch ? localeMatch[1] : "en";

  // Check if current path is protected
  const isProtectedRoute = PROTECTED_PATTERNS.some(
    (pattern) => pathname.includes(pattern)
  );

  // Check if current path is an auth route
  const isAuthRoute = AUTH_ROUTES.some((route) => pathname.includes(route));

  // 1. No token + protected route = redirect to signin
  if (isProtectedRoute && !token) {
    const signinUrl = new URL(`/${locale}/signin`, request.url);
    signinUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(signinUrl);
  }

  // 2. Has token + auth route = redirect to dashboard
  if (isAuthRoute && token) {
    return NextResponse.redirect(new URL(`/${locale}/dashboard`, request.url));
  }

  // 3. Allow request to continue
  return NextResponse.next();
}

export const config = {
  // Match all routes except static files and API routes
  matcher: [
    /*
     * Match all request paths except for:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico, robots.txt, sitemap.xml
     */
    "/((?!api|_next/static|_next/image|favicon.ico|robots.txt|sitemap.xml).*)",
  ],
};
