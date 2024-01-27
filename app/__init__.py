from fastapi import FastAPI

from .routers import decks, players
from .sql.models import Base
from .sql.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(players.router)
app.include_router(decks.router)
