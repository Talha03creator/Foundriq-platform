import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Database URL configuration
if os.environ.get("VERCEL"):
    # Neon PostgreSQL — persistent across cold starts
    # URL must NOT have sslmode/ssl params — asyncpg handles SSL via connect_args
    DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_njlskSY7e3AP@ep-blue-meadow-aicj8n2h-pooler.c-4.us-east-1.aws.neon.tech/neondb"
    IS_POSTGRES = True
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///foundriq.db")
    IS_POSTGRES = "postgresql" in DATABASE_URL or "postgres" in DATABASE_URL

SECRET_KEY = os.getenv("SECRET_KEY", "foundriq-super-secret-key-change-in-production-2024")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
