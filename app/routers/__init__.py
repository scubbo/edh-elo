from fastapi import APIRouter

from . import decks, games, players

api_router = APIRouter(prefix="/api")
html_router = APIRouter()

api_router.include_router(decks.api_router)
api_router.include_router(players.api_router)
api_router.include_router(games.api_router)

html_router.include_router(decks.html_router)
html_router.include_router(players.html_router)
html_router.include_router(games.html_router)
