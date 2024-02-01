from fastapi import APIRouter

from . import decks, players

api_router = APIRouter(prefix="/api")
html_router = APIRouter()

api_router.include_router(decks.api_router)
api_router.include_router(players.api_router)

html_router.include_router(decks.html_router)
html_router.include_router(players.html_router)
