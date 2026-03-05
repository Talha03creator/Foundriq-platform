import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Database URL configuration
# On Vercel (serverless), use the persistent Neon PostgreSQL database
# Locally, use SQLite for convenience
if os.environ.get("VERCEL"):
    # Neon PostgreSQL — persistent across cold starts
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://neondb_owner:npg_njlskSY7e3AP@ep-blue-meadow-aicj8n2h-pooler.c-4.us-east-1.aws.neon.tech/neondb?ssl=require"
    )
    # Ensure correct SQLAlchemy async driver prefix
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    elif DATABASE_URL.startswith("postgresql://") and "+asyncpg" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    # Local development — SQLite
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///foundriq.db")

SECRET_KEY = os.getenv("SECRET_KEY", "foundriq-super-secret-key-change-in-production-2024")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
