# Backend Coding Standards

## Project Standards Library

This document defines the coding standards, patterns, and best practices for the backend codebase.

---

## Architecture Principles

### 1. **Separation of Concerns**

```
app/
├── api/          # HTTP layer (routes, endpoints)
├── core/         # Configuration, security
├── crud/         # Database operations
├── db/           # Database connection
├── models/       # (Prisma handles this via schema.prisma)
└── schemas/      # Request/Response validation (Pydantic)
```

**Rule:** Each layer has a single responsibility.

### **Important: "Reserved Slots" for Enterprise Features**

The current folder structure includes **intentionally empty files** that serve as "Reserved Slots" for enterprise-grade features. These are not placeholders—they are **architectural commitments** to scalability and observability.

**Examples:**
- **`app/api/middleware/observability.py`** - Currently a placeholder for a Request-ID system that ensures every action is traceable across 100k+ users. This will implement distributed tracing, request correlation, and performance monitoring.
- **`app/crud/base.py`** - Base CRUD class that will automatically inject organization scoping into every query, preventing data leakage between tenants.
- **`app/core/config.py`** - Pydantic Settings class that validates all environment variables at startup, preventing silent failures in production.

**Why this matters:** When building multiple SaaS products from this starter kit, all products will use the same security patterns, observability standards, and architectural patterns. This ensures consistency and reduces technical debt.

### 2. **Multi-Tenancy First**

All database queries **must** include organization scoping:

```python
# ✅ CORRECT
users = await db.user.find_many(
    where={"organization_id": current_org.id}
)

# ❌ WRONG (security risk)
users = await db.user.find_many()  # Returns ALL users!
```

**Use:** `app/crud/base.py` provides automatic org scoping.

### 3. **Type Safety**

Always use type hints:

```python
# ✅ CORRECT
async def get_user(user_id: str) -> User:
    return await db.user.find_unique(where={"id": user_id})

# ❌ WRONG
async def get_user(user_id):
    return await db.user.find_unique(where={"id": user_id})
```

---

## File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| **Modules** | `snake_case.py` | `user_service.py` |
| **Classes** | `PascalCase` | `UserService` |
| **Functions** | `snake_case` | `get_user_by_id` |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_FILE_SIZE` |
| **Private** | `_leading_underscore` | `_internal_helper` |

---

## Code Organization

### **API Endpoints**

```python
# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
async def list_users(
    current_user: User = Depends(get_current_user)
):
    """List all users in the organization."""
    # Implementation
    pass
```

**Rules:**
- One file per resource (`users.py`, `organizations.py`)
- Use `APIRouter` for route groups
- Always include response models
- Use dependency injection for auth

### **CRUD Operations**

```python
# app/crud/user.py
from app.crud.base import CRUDBase
from prisma import Prisma

class CRUDUser(CRUDBase):
    async def get_by_email(
        self, db: Prisma, *, email: str
    ) -> User | None:
        return await db.user.find_unique(where={"email": email})

user = CRUDUser()
```

**Rules:**
- Inherit from `CRUDBase` for org scoping
- Use async/await for all database operations
- Return `None` when not found (not exceptions)

### **Pydantic Schemas**

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str | None = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
```

**Rules:**
- Separate schemas for Create/Update/Response
- Use `EmailStr`, `HttpUrl` for validation
- Response models exclude sensitive fields (passwords)

---

## Error Handling

### **Standard Exception Pattern**

```python
from fastapi import HTTPException

# ✅ CORRECT
if not user:
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

# ❌ WRONG
if not user:
    return {"error": "User not found"}  # Inconsistent
```

### **Custom Exceptions**

```python
# app/core/exceptions.py
class UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="User not found"
        )
```

---

## Security Standards

### **1. Authentication**

Always use dependency injection:

```python
from app.api.deps import get_current_active_user

@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_active_user)
):
    # User is authenticated and active
    pass
```

### **2. Authorization (RBAC)**

```python
from app.api.deps import require_permission

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_permission("CAN_DELETE_USERS"))
):
    # User has required permission
    pass
```

### **3. Password Hashing**

```python
from app.core.security import get_password_hash, verify_password

# Hash password
hashed = get_password_hash("plain_password")

# Verify password
is_valid = verify_password("plain_password", hashed)
```

**Never store plain passwords!**

---

## Database Standards

### **1. Use Prisma Client**

```python
# ✅ CORRECT
from prisma import Prisma

db = Prisma()
user = await db.user.create(data={...})

# ❌ WRONG (raw SQL)
await db.execute("INSERT INTO users ...")
```

### **2. Transactions**

```python
async with db.tx() as transaction:
    user = await transaction.user.create(data={...})
    org = await transaction.organization.create(data={...})
```

### **3. Query Optimization**

```python
# ✅ CORRECT (select only needed fields)
users = await db.user.find_many(
    select={"id": True, "email": True}
)

# ❌ WRONG (fetches all fields)
users = await db.user.find_many()
```

---

## Logging Standards

### **Structured Logging**

```python
import logging
from app.lib.logger import get_logger

logger = get_logger(__name__)

logger.info("User created", extra={
    "user_id": user.id,
    "organization_id": org.id
})
```

**Rules:**
- Use structured logging (JSON format)
- Include context (user_id, request_id)
- Never log sensitive data (passwords, tokens)

---

## Testing Standards

### **Test Structure**

```python
# tests/test_users.py
import pytest
from app.api.v1.endpoints.users import router

@pytest.mark.asyncio
async def test_create_user():
    # Arrange
    user_data = {"email": "test@example.com", "name": "Test"}
    
    # Act
    response = await router.post("/users", json=user_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

**Rules:**
- Use `pytest` and `pytest-asyncio`
- Follow Arrange-Act-Assert pattern
- Test both success and failure cases

---

## Documentation Standards

### **API Documentation**

```python
@router.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new user.
    
    - **email**: User's email address (must be unique)
    - **name**: User's full name (optional)
    - **password**: User's password (min 8 characters)
    
    Returns the created user (without password).
    """
    pass
```

**Rules:**
- Use docstrings for all endpoints
- Document parameters and return values
- Include examples for complex endpoints

---

## Environment Variables

### **Required Variables**

```env
# Database
DATABASE_URL=postgresql://...

# Security
JWT_SECRET_KEY=...
JWT_REFRESH_SECRET_KEY=...

# API Keys
GEMINI_API_KEY=...
OPENAI_API_KEY=...
STRIPE_SECRET_KEY=...

# App Config
ENVIRONMENT=development|production
CORS_ORIGINS=http://localhost:3000
```

**Rules:**
- Never commit `.env` files
- Use `app/core/config.py` for validation
- Document all required variables

---

## Git Workflow

### **Branch Naming**

- `main` - Production-ready code
- `develop` - Development branch
- `feature/user-authentication` - New features
- `fix/login-bug` - Bug fixes
- `refactor/database-layer` - Refactoring

### **Commit Messages**

```
feat: add user authentication endpoint
fix: resolve organization scoping bug
refactor: simplify CRUD base class
docs: update API documentation
```

---

## Performance Guidelines

1. **Use async/await** for all I/O operations
2. **Connection pooling** via Prisma (automatic)
3. **Pagination** for list endpoints
4. **Caching** for frequently accessed data
5. **Background tasks** for heavy operations

---

## Summary

- **Type safety** - Always use type hints
- **Security first** - Multi-tenancy, auth, validation
- **Consistent patterns** - Follow established conventions
- **Documentation** - Document all public APIs
- **Testing** - Write tests for critical paths

These standards ensure the codebase remains maintainable, secure, and scalable.
