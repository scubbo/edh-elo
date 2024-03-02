import csv
import datetime
import logging
from fastapi import APIRouter, Depends, Request, UploadFile
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..templates import jinja_templates
from ..sql import crud, schemas
from ..sql.database import get_db


LOGGER = logging.getLogger(__name__)

api_router = APIRouter(prefix="/seed", tags=["seed"])
html_router = APIRouter(
    prefix="/seed", include_in_schema=False, default_response_class=HTMLResponse
)


@api_router.post("/players")
def seed_players(file: UploadFile, db: Session = Depends(get_db)):
    file_contents = file.file.read().decode("utf-8").split("\n")
    reader = csv.reader(file_contents, delimiter=",")
    for row in reader:
        if not row:
            continue
        player_name = row[1]
        crud.create_player(db=db, player=schemas.PlayerCreate(name=player_name))
    return "OK!"


@api_router.post("/decks")
def seed_decks(file: UploadFile, db: Session = Depends(get_db)):
    file_contents = file.file.read().decode("utf-8").split("\n")
    reader = csv.DictReader(file_contents, delimiter=",")
    for row in reader:
        if not row:
            continue
        crud.create_deck(
            db=db,
            deck=schemas.DeckCreate(
                **{key: row[key] for key in ["name", "description", "owner_id"]}
            ),
        )
    return "OK!"


@api_router.post("/games")
def seed_games(file: UploadFile, db: Session = Depends(get_db)):
    file_contents = file.file.read().decode("utf-8").split("\n")
    reader = csv.DictReader(file_contents, delimiter=",")
    for row in reader:
        if not row:
            continue
        args = {
            key: row[key]
            for key in [
                "deck_id_1",
                "deck_id_2",
                "winning_deck_id",
                "number_of_turns",
                "first_player_out_turn",
                "win_type_id",
                "description",
            ]
        }
        args["date"] = datetime.datetime.strptime(row["date"], "%Y-%m-%d")

        for deck_id_num in ["deck_id_3", "deck_id_4", "deck_id_5", "deck_id_6"]:
            if deck_id := row[deck_id_num]:
                LOGGER.error(f"{deck_id_num} is {deck_id}")
                args[deck_id_num] = deck_id
        crud.create_game(
            db=db,
            game=schemas.GameCreate(**args),
        )
    return "OK!"


@html_router.get("/")
def main(request: Request, db=Depends(get_db)):
    return jinja_templates.TemplateResponse(
        request,
        "/seed.html",
    )
