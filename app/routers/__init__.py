from fastapi import APIRouter

from . import base, decks, games, players, seed

api_router = APIRouter(prefix="/api")
html_router = APIRouter()

api_router.include_router(decks.api_router)
api_router.include_router(players.api_router)
api_router.include_router(games.api_router)
api_router.include_router(seed.api_router)

html_router.include_router(decks.html_router)
html_router.include_router(players.html_router)
html_router.include_router(games.html_router)
html_router.include_router(seed.html_router)

html_router.include_router(base.html_router)
