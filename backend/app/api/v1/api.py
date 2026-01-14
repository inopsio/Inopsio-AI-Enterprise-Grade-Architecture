"""
Inopsio AI Enterprise - API Router
Central hub that connects all endpoint modules.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth

api_router = APIRouter()

# Auth routes (login, test-token)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Add more routers as you build features:
# from app.api.v1.endpoints import users, organizations, domains
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
# api_router.include_router(domains.router, prefix="/domains", tags=["domains"])
