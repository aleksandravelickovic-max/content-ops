from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .database import init_db
from .routes import review, api, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Content Ops Review Portal", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(review.router)
app.include_router(api.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return RedirectResponse(url="/admin/")

