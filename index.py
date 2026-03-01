import sys
import os
import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="FoundrIQ - Diagnostic")

@app.get("/")
def diagnostic():
    results = {}
    
    # Test Dependency Imports
    deps = [
        "sqlalchemy", 
        "aiosqlite", 
        "passlib.context", 
        "jose", 
        "dotenv", 
        "openai", 
        "pydantic", 
        "bcrypt",
        "multipart",
        "email_validator"
    ]
    
    for dep in deps:
        try:
            __import__(dep)
            results[dep] = "OK"
        except ImportError as e:
            results[dep] = f"ERROR: {str(e)}"

    return {
        "status": "Diagnostic API Running",
        "python_version": sys.version,
        "import_tests": results
    }
