import uvicorn

from app import *



uvicorn.run("app:app", host="127.0.0.1", port=6006, log_level="info")
