"""
Inopsio AI Enterprise - Token Schemas
Pydantic models for JWT token payloads.
"""
from pydantic import BaseModel


class Token(BaseModel):
    """Response model for login endpoint."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    The payload inside a JWT token.
    
    - sub: The subject (user_id)
    - exp: Expiration timestamp (handled by jose)
    """
    sub: str | None = None
