from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.sql import models

from ..templates import jinja_templates
from ..sql import crud, schemas
from ..sql.database import get_db

from .players import list_players

api_router = APIRouter(prefix="/deck", tags=["deck"])
html_router = APIRouter(
    prefix="/deck", include_in_schema=False, default_response_class=HTMLResponse
)


########
# API Routes
########


@api_router.post("/", response_model=schemas.Deck, status_code=201)
def create_deck(deck: schemas.DeckCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_id(db, deck.owner_id)
    if db_player is None:
        raise HTTPException(
            status_code=400, detail=f"Owner id {deck.owner_id} not found"
        )

    return crud.create_deck(db=db, deck=deck)


@api_router.get("/list", response_model=list[schemas.Deck])
def list_decks(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return crud.get_decks(db, skip=skip, limit=limit)


@api_router.get("/{deck_id}", response_model=schemas.Deck)
def read_deck(deck_id: int, db=Depends(get_db)):
    print(deck_id)
    db_deck = crud.get_deck_by_id(db, deck_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return db_deck


@api_router.delete("/{deck_id}", status_code=204)
def delete_deck(deck_id: str, db=Depends(get_db)):
    crud.delete_deck_by_id(db, int(deck_id))


########
# HTML Routes
########


@html_router.get("/create")
def deck_create_html(request: Request, db=Depends(get_db)):
    players = list_players(db=db)
    return jinja_templates.TemplateResponse(
        request, "decks/create.html", {"players": players}
    )


# TODO - pagination
@html_router.get("/list")
def decks_html(request: Request, db=Depends(get_db)):
    decks = list_decks(db=db)
    return jinja_templates.TemplateResponse(
        request, "decks/list.html", {"decks": decks}
    )


# This must be after the static-path routes, lest it take priority over them
@html_router.get("/{deck_id}")
def deck_html(request: Request, deck_id: str, db=Depends(get_db)):
    deck_info = read_deck(deck_id, db)
    deck_score_history = _build_deck_score_history(deck_id, db)
    return jinja_templates.TemplateResponse(
        request,
        "decks/detail.html",
        {
            "deck": deck_info,
            "owner": deck_info.owner,
            "game_history": deck_score_history,
        },
    )


def _build_deck_score_history(deck_id: str, db: Session):
    # This is...horrible.
    # But I can't find a way to execute a join _in_ SQLAlchemy in such a way that the response is actual objects rather
    # than the underlying rows
    # (https://stackoverflow.com/questions/78596316/)
    games_involving_this_deck = (
        db.query(models.Game)
        .filter(
            or_(*[getattr(models.Game, f"deck_id_{i+1}") == deck_id for i in range(6)])
        )
        .all()
    )
    # Having found the games, then add the score for this deck after that game
    return [
        {
            "game": game,
            "score": db.query(models.EloScore)
            .filter(
                and_(
                    models.EloScore.after_game_id == game.id,
                    models.EloScore.deck_id == deck_id,
                )
            )
            .first()
            .score,
        }
        for game in games_involving_this_deck
    ]
