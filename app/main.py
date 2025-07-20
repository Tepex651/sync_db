import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.v1.info import router as info_router
from app.config.logger import setup_logging
from app.db.session import create_tables
from app.middlewares.logger import LoggingMiddleware
from app.service.update import UpdateService


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    await create_tables()
    update_service = UpdateService()

    task = asyncio.create_task(update_service.run_periodic_updates())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.include_router(info_router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=5555)
