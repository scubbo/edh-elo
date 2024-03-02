import json
from functional import seq
from typing import List, Mapping


from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.routers.decks import list_decks
from app.sql import models
from .players import list_players
from ..templates import jinja_templates
from ..sql import crud, schemas
from ..sql.database import get_db

api_router = APIRouter(prefix="/game", tags=["game"])
html_router = APIRouter(
    prefix="/game", include_in_schema=False, default_response_class=HTMLResponse
)

########
# API Routes
########


@api_router.post("/", response_model=schemas.Game, status_code=201)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    return crud.create_game(db=db, game=game)


@api_router.get("/list", response_model=list[schemas.Game])
def list_games(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return crud.get_games(db, skip=skip, limit=limit)


@api_router.get("/{game_id}", response_model=schemas.Game)
def read_game(game_id: int, db=Depends(get_db)):
    db_game = crud.get_game_by_id(db, game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game


@api_router.delete("/{game_id}", status_code=204)
def delete_game(game_id: str, db=Depends(get_db)):
    crud.delete_game_by_id(db, int(game_id))


########
# HTML Routes
########


@html_router.get("/create", response_class=HTMLResponse)
def game_create_html(request: Request, db=Depends(get_db)):
    players = list_players(db=db)
    return jinja_templates.TemplateResponse(
        request,
        "games/create.html",
        {
            "players": players,
            # `json.dumps` is necessary because otherwise
            # the keys are surrounded with single-quotes,
            # on which JavaScript's `JSON.parse` will choke.
            "player_decks": json.dumps(
                {
                    str(player.id): [
                        {key: getattr(deck, key) for key in ["id", "name"]}
                        for deck in player.decks
                    ]
                    for player in players
                }
            ),
        },
    )


# TODO - pagination
@html_router.get("/list")
def games_html(request: Request, db=Depends(get_db)):
    games = list_games(db=db)
    decks = list_decks(db=db)
    decks_by_id = {deck.id: deck for deck in decks}
    game_names = {game.id: _build_game_deck_names(game, decks_by_id) for game in games}
    return jinja_templates.TemplateResponse(
        request,
        "games/list.html",
        {"games": games, "decks_by_id": decks_by_id, "game_names": game_names},
    )


def _build_game_deck_names(
    game: models.Game, decks_by_id: Mapping[int, models.Deck]
) -> List[str]:
    return (
        seq(range(6))
        .map(lambda i: i + 1)
        .map(lambda i: f"deck_id_{i}")
        .map(lambda key: getattr(game, key))
        .filter(lambda x: x)
        .map(lambda deck_id: decks_by_id[deck_id])
        .map(lambda deck: deck.name)
    )


# This must be after the static-path routes, lest it take priority over them
@html_router.get("/{game_id}")
def game_html(request: Request, game_id: str, db=Depends(get_db)):
    game_info = read_game(game_id, db)
    return jinja_templates.TemplateResponse(
        request, "games/detail.html", {"game": game_info}
    )
