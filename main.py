from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

from core.db_helper import db_helper
from core.models import Base
from core.config import settings

from api.users.views import router as user_router
from api.competitions.views import router as competitions_router
from api.results.views import router as results_router
from api.auth.views import router as auth_router
from api.cv.views import router as video_router
from api.icons.test import router as icons_router



@asynccontextmanager
async def lifespan(app: FastAPI):

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix=settings.api_prefix)
app.include_router(competitions_router, prefix=settings.api_prefix)
app.include_router(results_router, prefix=settings.api_prefix)
app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(video_router, prefix=settings.api_prefix)
app.include_router(icons_router, prefix=settings.api_prefix)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- поменять в проде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
