"""
Vercel FastAPI Entrypoint
========================
Vercel auto-detects `app = FastAPI()` from index.py at the project root.
This file re-exports the app from the server package.
"""
import os
import sys

# Ensure the project root is in the Python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from server.main import app
