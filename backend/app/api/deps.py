"""
Inopsio AI Enterprise - API Dependencies
The "Security Guard" that validates JWT tokens and extracts user/organization context.
"""
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from prisma import Prisma

from app.core.config import settings
from app.db.session import prisma
from app.schemas.token import TokenPayload

# The entry point for OAuth2 - looks for "Authorization: Bearer <token>"
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


async def get_db() -> Generator:
    """Provides the Prisma database instance to routes."""
    if not prisma.is_connected():
        await prisma.connect()
    yield prisma


async def get_current_user(
    db: Prisma = Depends(get_db),
    token: str = Depends(reusable_oauth2)
):
    """
    Validates the JWT token and returns the current user.
    If the token is invalid, it raises a 401 Unauthorized error.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if token_data.sub is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = await db.user.find_unique(where={"id": token_data.sub})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
    current_user = Depends(get_current_user),
):
    """Checks if the authenticated user is still active."""
    if not current_user.isActive:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_organization_id(
    current_user = Depends(get_current_active_user),
    db: Prisma = Depends(get_db),
) -> str:
    """
    Extracts the organization_id for the current request context.
    This is the 'Key' used by your CRUDBase to filter data.
    """
    # Get user's memberships with organization info
    memberships = await db.member.find_many(
        where={"userId": current_user.id},
        include={"organization": True}
    )
    
    if not memberships:
        raise HTTPException(status_code=403, detail="User has no organization")
    
    # Return the first organization (primary org)
    return memberships[0].organizationId
