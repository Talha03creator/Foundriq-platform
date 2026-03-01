import os
import sys
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Ensure the project root is in the Python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import the actual app from the server module
try:
    from server.main import app
except Exception as e:
    app = FastAPI()
    @app.get("/{path:path}")
    def catch_all(path: str):
        return JSONResponse(status_code=500, content={"error": "Import failed", "details": str(e)})

