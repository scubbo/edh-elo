from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..sql import crud, schemas
from ..sql.database import get_db

router = APIRouter()


@router.post("/deck", response_model=schemas.Deck, tags=["deck"], status_code=201)
def create_deck(deck: schemas.DeckCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_id(db, deck.owner_id)
    if db_player is None:
        raise HTTPException(status_code=400, detail=f"Owner id {deck.owner_id} not found")

    return crud.create_deck(db=db, deck=deck)


@router.get("/deck/{deck_id}", response_model=schemas.Deck, tags=["deck"])
def read_deck(deck_id: str, db = Depends(get_db)):
    db_deck = crud.get_deck_by_id(db, deck_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return db_deck


@router.get("/decks", response_model=list[schemas.Deck], tags=["deck"])
def list_decks(skip: int = 0, limit: int = 100, db = Depends(get_db)):
    return crud.get_decks(db, skip=skip, limit=limit)


@router.delete("/deck/{deck_id}", tags=["deck"], status_code=204)
def delete_deck(deck_id: str, db = Depends(get_db)):
    crud.delete_deck_by_id(db, int(deck_id))
