from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..templates import jinja_templates
from ..sql import crud, schemas
from ..sql.database import get_db

api_router = APIRouter(prefix="/player", tags=["player"])
html_router = APIRouter(
    prefix="/player",
    include_in_schema=False,
    default_response_class=HTMLResponse)

########
# API Routes
########


@api_router.post("/", response_model=schemas.Player, status_code=201)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return crud.create_player(db=db, player=player)


@api_router.get("/list", response_model=list[schemas.Player])
def list_players(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return crud.get_players(db, skip=skip, limit=limit)


@api_router.get("/{player_id}", response_model=schemas.Player)
def read_player(player_id: int, db=Depends(get_db)):
    db_player = crud.get_player_by_id(db, player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player


@api_router.delete("/{player_id}", status_code=204)
def delete_player(player_id: str, db=Depends(get_db)):
    crud.delete_player_by_id(db, int(player_id))


########
# HTML Routes
########

@html_router.get("/create")
def player_create_html(request: Request, db=Depends(get_db)):
    return jinja_templates.TemplateResponse(request, "players/create.html")

@html_router.get("/list", response_class=HTMLResponse)
def player_list_html(request: Request, db=Depends(get_db)):
    players = list_players(db=db)
    return jinja_templates.TemplateResponse(
        request, "players/list.html", {"players": players})


# This must be after the static-path routes, lest it take priority over them
@html_router.get("/{player_id}")
def player_html(request: Request, player_id: str, db=Depends(get_db)):
    player_info = read_player(player_id, db)
    return jinja_templates.TemplateResponse(
        request, "players/detail.html", {"player": player_info}
    )
