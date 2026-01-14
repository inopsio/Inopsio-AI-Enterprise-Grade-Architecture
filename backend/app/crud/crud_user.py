"""
Inopsio AI Enterprise - User CRUD
Specialized CRUD operations for users with password hashing.
"""
from typing import Optional, Any
from prisma import Prisma

from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[Any, UserCreate, UserUpdate]):
    """
    User CRUD with password hashing support.
    
    Unlike standard CRUD, this class:
    - Hashes passwords before saving
    - Provides email-based lookup
    - Includes authentication helper
    """
    
    async def get_by_email(self, db: Prisma, *, email: str) -> Optional[Any]:
        """Find a user by their email address."""
        return await db.user.find_unique(where={"email": email})

    async def create(self, db: Prisma, *, obj_in: UserCreate) -> Any:
        """
        Create a new user with hashed password.
        Overrides base create to handle password transformation.
        """
        db_obj_data = obj_in.model_dump()
        # Hash the password before saving
        password = db_obj_data.pop("password")
        db_obj_data["hashedPassword"] = get_password_hash(password)
        
        return await db.user.create(data=db_obj_data)

    async def authenticate(
        self, db: Prisma, *, email: str, password: str
    ) -> Optional[Any]:
        """
        Verify email and password combination.
        Returns the user if valid, None otherwise.
        """
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashedPassword):
            return None
        return user

    async def update(
        self, db: Prisma, *, id: str, obj_in: UserUpdate
    ) -> Optional[Any]:
        """
        Update user with optional password change.
        If password is provided, it gets hashed.
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Hash password if being updated
        if "password" in update_data:
            password = update_data.pop("password")
            update_data["hashedPassword"] = get_password_hash(password)
        
        return await db.user.update(
            where={"id": id},
            data=update_data
        )


# Singleton instance for use throughout the app
user = CRUDUser("user")
