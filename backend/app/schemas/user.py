"""
Inopsio AI Enterprise - User Schemas
Pydantic models for User request/response validation.
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """Base user properties shared across schemas."""
    email: EmailStr
    fullName: str | None = None


class UserCreate(UserBase):
    """Schema for creating a new user (includes password)."""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user (all fields optional)."""
    email: EmailStr | None = None
    fullName: str | None = None
    password: str | None = None


class UserOut(UserBase):
    """
    Schema for user responses (safe data only).
    Never includes password or hashed password.
    """
    id: str
    isActive: bool
    createdAt: datetime

    class Config:
        from_attributes = True
