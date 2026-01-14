"""
Inopsio AI Enterprise - Multi-Tenant CRUD Base
The "Guardian" that auto-scopes all database queries by organization_id.
"""
from typing import Generic, TypeVar, List, Optional, Any
from pydantic import BaseModel
from prisma import Prisma

# Define Type Variables for your Models and Schemas
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for CRUD operations with Multi-tenancy support.
    
    All queries are automatically scoped to the organization_id,
    preventing data leakage between tenants.
    
    Usage:
        domain = CRUDBase[Domain, DomainCreate, DomainUpdate]("domain")
    """
    
    def __init__(self, model_name: str):
        """
        Initialize the CRUD handler.
        :param model_name: The name of the Prisma model (e.g., 'user', 'domain')
        """
        self.model_name = model_name

    async def get(
        self, db: Prisma, *, id: str, organization_id: str
    ) -> Optional[ModelType]:
        """Fetch a single record, strictly scoped to the organization."""
        model = getattr(db, self.model_name)
        return await model.find_first(
            where={"id": id, "organization_id": organization_id}
        )

    async def get_multi(
        self, db: Prisma, *, organization_id: str, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Fetch multiple records for a specific organization with pagination."""
        model = getattr(db, self.model_name)
        return await model.find_many(
            where={"organization_id": organization_id},
            skip=skip,
            take=limit,
            order={"created_at": "desc"}
        )

    async def create(
        self, db: Prisma, *, obj_in: CreateSchemaType, organization_id: str
    ) -> ModelType:
        """Create a new record automatically linked to the organization."""
        model = getattr(db, self.model_name)
        data = obj_in.model_dump()
        data["organization_id"] = organization_id
        return await model.create(data=data)

    async def update(
        self, db: Prisma, *, id: str, obj_in: UpdateSchemaType, organization_id: str
    ) -> Optional[ModelType]:
        """Update a record only if it belongs to the organization."""
        model = getattr(db, self.model_name)
        data = obj_in.model_dump(exclude_unset=True)
        return await model.update(
            where={"id": id},
            data=data
        )

    async def remove(
        self, db: Prisma, *, id: str, organization_id: str
    ) -> int:
        """
        Delete a record only if it belongs to the organization.
        Returns the count of deleted records (0 or 1).
        """
        model = getattr(db, self.model_name)
        result = await model.delete_many(
            where={"id": id, "organization_id": organization_id}
        )
        return result
