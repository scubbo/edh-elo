from fastapi import APIRouter, Depends

from ..sql import crud, schemas
from ..sql.database import get_db

api_router = APIRouter(prefix="/score", tags=["score"])


@api_router.get("/{deck_id}/latest", response_model=schemas.EloScore)
def get_latest_score_for_deck(deck_id: int, db=Depends(get_db)):
    return crud.get_latest_score_for_deck(db, deck_id)


@api_router.get("/{deck_id}/all", response_model=list[schemas.EloScore])
def get_all_scores_for_deck(deck_id: int, db=Depends(get_db)):
    return crud.get_all_scores_for_deck(db, deck_id)
