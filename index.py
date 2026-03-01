"""
Vercel FastAPI Entrypoint
========================
Vercel's native FastAPI runtime auto-detects `app = FastAPI()`
from specific entrypoints: index.py, app.py, or server.py
(at root, src/, or app/ directories).

This file re-exports the FastAPI app from api/main.py
so Vercel can find it. No logic lives here.
"""
import os
import sys

# Ensure the project root is in the Python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from api.main import app
