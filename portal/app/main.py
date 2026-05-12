from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .config import SECRET_KEY
from .database import init_db
from .routes import review, api, admin, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Content Ops Review Portal", lifespan=lifespan)

# Session middleware for OAuth — signed cookies, httponly, samesite=lax
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="contentops_session",
    same_site="lax",
    https_only=False,  # Set True behind HTTPS in production
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(auth.router)
app.include_router(review.router)
app.include_router(api.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return RedirectResponse(url="/admin/")

