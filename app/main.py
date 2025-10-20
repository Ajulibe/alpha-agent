from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.routes import router

# from .services.core.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # try:
    #     start_scheduler()
    # except Exception as e:
    #     print(f"Failed to start scheduler: {e}")
    yield


app = FastAPI(title="Alpha Agents API", lifespan=lifespan)
app.include_router(router)
