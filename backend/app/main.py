"""
Inopsio AI Enterprise - FastAPI Entry Point
The "Manager" of the Warehouse that handles CORS, Prisma lifecycle, and observability.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid
import re

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import prisma


# 1. LIFESPAN: The 2026 standard for managing connections
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages database connection lifecycle."""
    # Startup: Open the database connection
    await prisma.connect()
    yield
    # Shutdown: Clean up and close connection
    await prisma.disconnect()


app = FastAPI(
    title="Inopsio AI Enterprise API",
    version="1.0.0",
    lifespan=lifespan
)


# 2. CORS: Dynamic origin validator for Vercel preview URLs
# Note: Wildcards don't work with allow_credentials=True
def is_allowed_origin(origin: str) -> bool:
    """
    Validates if an origin is allowed.
    Supports explicit origins from settings AND Vercel preview URLs.
    """
    if not origin:
        return False
    
    # Check explicit origins from settings
    if origin in settings.CORS_ORIGINS:
        return True
    
    # Allow Vercel preview URLs (pattern: https://*.vercel.app)
    if re.match(r"^https://[\w-]+\.vercel\.app$", origin):
        return True
    
    # Allow localhost in development
    if origin.startswith("http://localhost:"):
        return True
    
    return False


# Custom CORS middleware that validates origins dynamically
@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    """Dynamic CORS validation for Vercel preview URLs."""
    origin = request.headers.get("origin")
    
    # Handle preflight requests
    if request.method == "OPTIONS":
        if origin and is_allowed_origin(origin):
            response = await call_next(request)
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, X-Request-ID"
            response.headers["Access-Control-Expose-Headers"] = "X-Request-ID, X-Process-Time"
            return response
    
    response = await call_next(request)
    
    # Add CORS headers for allowed origins
    if origin and is_allowed_origin(origin):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Expose-Headers"] = "X-Request-ID, X-Process-Time"
    
    return response


# 3. OBSERVABILITY: Request tracking for 100k+ DAU
@app.middleware("http")
async def add_process_time_and_request_id(request: Request, call_next):
    """Adds timing and unique ID to every request for debugging and tracing."""
    start_time = time.time()
    
    # Use client-provided request ID if present, otherwise generate one
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    
    # Process the request
    response = await call_next(request)
    
    # Add headers for debugging
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id
    return response


# 4. ROUTER: Connect the API endpoints
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring systems."""
    return {"status": "healthy", "version": "1.0.0"}
