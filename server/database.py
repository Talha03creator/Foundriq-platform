import ssl as _ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from server.config import DATABASE_URL, IS_POSTGRES

# Configure engine
engine_kwargs = {"echo": False}

if IS_POSTGRES:
    # asyncpg requires ssl=True passed via connect_args for Neon PostgreSQL
    ctx = _ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = _ssl.CERT_NONE
    engine_kwargs["connect_args"] = {"ssl": ctx}

engine = create_async_engine(DATABASE_URL, **engine_kwargs)
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
