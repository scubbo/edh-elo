from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..sql import crud, schemas
from ..sql.database import get_db

router = APIRouter()


@router.post("/player", response_model=schemas.Player, tags=["player"], status_code=201)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return crud.create_player(db=db, player=player)


@router.get("/player/{player_id}", response_model=schemas.Player, tags=["player"])
def read_player(player_id: str, db = Depends(get_db)):
    db_player = crud.get_player_by_id(db, player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player


@router.get("/players", response_model=list[schemas.Player], tags=["player"])
def list_players(skip: int = 0, limit: int = 100, db = Depends(get_db)):
    return crud.get_players(db, skip=skip, limit=limit)


@router.delete("/player/{player_id}", tags=["player"], status_code=204)
def delete_player(player_id: str, db = Depends(get_db)):
    crud.delete_player_by_id(db, int(player_id))
