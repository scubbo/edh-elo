import json

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from .players import list_players
from ..templates import jinja_templates
from ..sql import crud, schemas
from ..sql.database import get_db

api_router = APIRouter(prefix="/game", tags=["game"])
html_router = APIRouter(prefix="/game", include_in_schema=False)

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


@html_router.get("/create", response_class=HTMLResponse)
def game_create_html(request: Request, db=Depends(get_db)):
    players = list_players(db=db)
    return jinja_templates.TemplateResponse(
        request, "games/create.html", {
            "players": players,
            # `json.dumps` is necessary because otherwise
            # the keys are surrounded with single-quotes,
            # on which JavaScript's `JSON.parse` will choke.
            "player_decks": json.dumps({
                str(player.id): [{
                    key: getattr(deck, key)
                    for key in ['id', 'name']
                } for deck in player.decks]
                for player in players
            })
        })


# TODO - pagination
@html_router.get("/list", response_class=HTMLResponse)
def games_html(request: Request, db=Depends(get_db)):
    games = list_games(db=db)
    return jinja_templates.TemplateResponse(
        request, "games/list.html", {"games": games}
    )


# This must be after the static-path routes, lest it take priority over them
@html_router.get("/{game_id}", response_class=HTMLResponse)
def game_html(request: Request, game_id: str, db=Depends(get_db)):
    game_info = read_game(game_id, db)
    return jinja_templates.TemplateResponse(
        request, "games/detail.html", {"game": game_info}
    )