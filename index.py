"""
Vercel FastAPI Entrypoint
========================
"""
import os
import sys
import traceback

# Ensure the project root is in the Python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Try to import the full app; if it fails, serve a diagnostic app
try:
    from server.main import app
except Exception as e:
    # Fallback: create a minimal diagnostic app so we can see the error
    app = FastAPI(title="FoundrIQ - Diagnostic Mode")

    error_detail = {
        "error": str(e),
        "traceback": traceback.format_exc(),
        "python_version": sys.version,
        "sys_path": sys.path[:5],
        "cwd": os.getcwd(),
        "files_in_root": os.listdir(ROOT_DIR)[:20] if os.path.exists(ROOT_DIR) else [],
    }

    @app.get("/")
    async def diagnostic_root():
        return JSONResponse(content={
            "status": "DIAGNOSTIC MODE - Full app failed to load",
            **error_detail
        })

    @app.get("/{path:path}")
    async def diagnostic_catch_all(path: str):
        return JSONResponse(content={
            "status": "DIAGNOSTIC MODE - Full app failed to load",
            "requested_path": path,
            **error_detail
        })
