from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..templates import jinja_templates, _jsonify
from ..sql import crud, schemas
from ..sql.database import get_db

from .players import read_player, list_players

api_router = APIRouter(tags=["deck"])
html_router = APIRouter(include_in_schema=False)

@api_router.post("/deck", response_model=schemas.Deck, status_code=201)
def create_deck(deck: schemas.DeckCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_id(db, deck.owner_id)
    if db_player is None:
        raise HTTPException(status_code=400, detail=f"Owner id {deck.owner_id} not found")

    return crud.create_deck(db=db, deck=deck)


@api_router.get("/deck/{deck_id}", response_model=schemas.Deck)
def read_deck(deck_id: str, db = Depends(get_db)):
    db_deck = crud.get_deck_by_id(db, deck_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return db_deck


@api_router.get("/decks", response_model=list[schemas.Deck])
def list_decks(skip: int = 0, limit: int = 100, db = Depends(get_db)):
    return crud.get_decks(db, skip=skip, limit=limit)


@api_router.delete("/deck/{deck_id}", status_code=204)
def delete_deck(deck_id: str, db = Depends(get_db)):
    crud.delete_deck_by_id(db, int(deck_id))


@html_router.get("/deck/create", response_class=HTMLResponse)
def deck_create_html(request: Request, db = Depends(get_db)):
    players = list_players(db=db)
    return jinja_templates.TemplateResponse(
        request,
        "deck_create.html",
        {
            "players": players
        }
    )


@html_router.get("/deck/{deck_id}", response_class=HTMLResponse)
def deck_html(request: Request, deck_id: str, db = Depends(get_db)):
    deck_info = read_deck(deck_id, db)
    return jinja_templates.TemplateResponse(
        request,
        "deck_detail.html",
        {
            "deck": _jsonify(deck_info),
            "owner": _jsonify(deck_info.owner)
        }
    )


# TODO - pagination
@html_router.get("/decks", response_class=HTMLResponse)
def decks_html(request: Request, db = Depends(get_db)):
    decks = list_decks(db=db)
    print(decks)
    return jinja_templates.TemplateResponse(
        request,
        "deck_list.html",
        {
            # TODO - investigate if there are any issues to passing the "live" object into the
            # template, as opposed to the `_jsonify`'d one.
            "decks": decks
        }
    )