from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from server.config import DATABASE_URL

# For PostgreSQL with asyncpg, we need to handle SSL
connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args = {}
elif "asyncpg" in DATABASE_URL:
    # asyncpg handles SSL via the connection string params
    pass

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

_db_initialized = False


class Base(DeclarativeBase):
    pass


async def get_db():
    global _db_initialized
    if not _db_initialized:
        try:
            await init_db()
            _db_initialized = True
        except Exception as e:
            print(f"DB init warning: {e}")

    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
