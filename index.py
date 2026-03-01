import sys
import os
import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="FoundrIQ - Module Diagnostic")

@app.get("/")
def diagnostic():
    results = {}

    import_steps = [
        "server.config",
        "server.database",
        "server.auth.security",
        "server.models.user",
        "server.models.project",
        "server.models.report",
        "server.routes.auth",
        "server.routes.projects",
        "server.routes.analysis",
        "server.routes.dashboard",
        "server.main"
    ]

    for step in import_steps:
        try:
            __import__(step)
            results[step] = "OK"
        except Exception as e:
            results[step] = f"ERROR: {type(e).__name__} - {str(e)}"
            results[f"{step}_traceback"] = traceback.format_exc()
            break  # Stop at first failure since subsequent imports might depend on it

    return {
        "status": "Diagnostic API Running",
        "python_version": sys.version,
        "import_tests": results
    }
