import json
import logging
from functional import seq
from typing import List, Mapping


from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.routers.decks import list_decks
from app.sql import models
from .players import list_players
from ..elo import rerank
from ..sql import crud, schemas
from ..sql.database import get_db
from ..templates import jinja_templates

api_router = APIRouter(prefix="/game", tags=["game"])
html_router = APIRouter(
    prefix="/game", include_in_schema=False, default_response_class=HTMLResponse
)

LOGGER = logging.getLogger(__name__)

########
# API Routes
########


@api_router.post("/", response_model=schemas.Game, status_code=201)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    created_game = crud.create_game(db=db, game=game)

    # Update ELO scores
    last_score = (
        db.query(models.EloScore).order_by(models.EloScore.after_game_id.desc()).first()
    )
    if last_score:
        last_scored_game_id = last_score.after_game_id
    else:
        last_scored_game_id = 0
    if created_game.id != last_scored_game_id + 1:
        # TODO - better error reporting?
        LOGGER.error(
            f"Created a game with id {created_game.id}, which is not after the last-scored-game-id {last_scored_game_id}. ELO calculation paused."
        )
        return created_game

    deck_ids = [id for id in [getattr(game, f"deck_id_{n+1}") for n in range(6)] if id]
    print(f"DEBUG - {deck_ids=}")
    deck_scores_before_this_game = [
        crud.get_latest_score_for_deck(db, deck_id) for deck_id in deck_ids
    ]
    new_scores = rerank(
        deck_scores_before_this_game, deck_ids.index(game.winning_deck_id)
    )
    for score, deck_id in zip(new_scores, deck_ids):
        db.add(
            models.EloScore(after_game_id=created_game.id, deck_id=deck_id, score=score)
        )
        db.commit()
    return created_game


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
    win_types = db.query(models.WinType).all()
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
            "win_types": win_types,
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
