"""
Run MEMEKRAL API Server
Usage: python run_api.py
"""
import os
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.server:app",
        host="0.0.0.0",
        port=int(os.getenv("API_PORT", "8000")),
        reload=os.getenv("ENV", "development") == "development",
    )
