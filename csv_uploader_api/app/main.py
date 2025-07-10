from fastapi import FastAPI, Request
from app.api.endpoints import router as api_router
from app.utils.logger import setup_logging
import logging

setup_logging()

app = FastAPI(title="CSV Uploader API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("api_logger")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url} - {response.status_code}")
    return response

app.include_router(api_router)
