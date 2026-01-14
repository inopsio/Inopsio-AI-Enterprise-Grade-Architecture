"""
Inopsio AI Enterprise - Database Session
Manages the Prisma client lifecycle for async database operations.
"""
from prisma import Prisma

# Global Prisma client instance
prisma = Prisma()


async def get_db():
    """
    Dependency injection for database access.
    Usage in endpoints:
    
    @router.get("/users")
    async def get_users(db: Prisma = Depends(get_db)):
        users = await db.user.find_many()
        return users
    """
    if not prisma.is_connected():
        await prisma.connect()
    return prisma
