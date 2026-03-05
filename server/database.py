import ssl as _ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from server.config import DATABASE_URL, IS_POSTGRES


class Base(DeclarativeBase):
    pass


# Lazy engine initialization — don't connect until first request
_engine = None
_async_session = None
_db_initialized = False


def _get_engine():
    global _engine
    if _engine is None:
        kwargs = {"echo": False, "pool_pre_ping": True}
        if IS_POSTGRES:
            ctx = _ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = _ssl.CERT_NONE
            kwargs["connect_args"] = {"ssl": ctx}
        _engine = create_async_engine(DATABASE_URL, **kwargs)
    return _engine


def _get_session_maker():
    global _async_session
    if _async_session is None:
        _async_session = async_sessionmaker(
            _get_engine(), class_=AsyncSession, expire_on_commit=False
        )
    return _async_session


async def get_db():
    global _db_initialized
    if not _db_initialized:
        try:
            await init_db()
            _db_initialized = True
        except Exception as e:
            print(f"DB init warning: {e}")

    session_maker = _get_session_maker()
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    engine = _get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
