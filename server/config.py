import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
# If running on Vercel (which uses Linux), we must use the ephemeral /tmp directory
# since the rest of the filesystem is read-only.
if os.environ.get("VERCEL") or not sys.platform.startswith("win"):
    # Always force /tmp/ for serverless
    DATABASE_URL = "sqlite+aiosqlite:////tmp/foundriq.db"
else:
    # Use local file for development
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///foundriq.db")
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))


