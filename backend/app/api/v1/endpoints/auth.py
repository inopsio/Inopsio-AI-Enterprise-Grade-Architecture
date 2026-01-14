"""
Inopsio AI Enterprise - Auth Endpoints
Handles login and token validation.
"""
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from prisma import Prisma

from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas.token import Token
from app.schemas.user import UserOut

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_access_token(
    db: Prisma = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    
    - **username**: User's email address
    - **password**: User's password
    
    Returns a JWT access token.
    """
    # 1. Find the user by email
    user = await db.user.find_unique(where={"email": form_data.username})
    
    # 2. Verify password
    if not user or not security.verify_password(form_data.password, user.hashedPassword):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Check if user is active
    if not user.isActive:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # 4. Create and return the access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/test-token", response_model=UserOut)
async def test_token(
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Test if the access token is valid and return the current user.
    Useful for frontend to verify auth state on app load.
    """
    return current_user
