from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.errors import BetgameError
from app.jobs.scheduler import scheduler, start_scheduler
from app.routes import auth, bets, matches, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    scheduler.shutdown()


app = FastAPI(title="Sports Bets API", lifespan=lifespan)

app.include_router(bets.router)
app.include_router(matches.router)
app.include_router(auth.router)
app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(BetgameError)
async def handle_betgame_error(request: Request, exc: BetgameError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/")
def root():
    return {"message": "API läuft"}
