import csv
import datetime
import logging

from collections import defaultdict


from fastapi import APIRouter, Depends, Request, UploadFile
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from .games import create_game
from ..templates import jinja_templates
from ..sql import crud, schemas
from ..sql.database import get_db
from ..sql.models import Format, WinType


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


@api_router.post("/all_in_one")
def all_in_one(file: UploadFile, db: Session = Depends(get_db)):
    file_contents = file.file.read().decode("utf-8").split("\n")
    reader = csv.DictReader(file_contents, delimiter=",")

    # Mapping from name to set-of-owned-decks
    # (Set rather than list so that we can blindly `.add`)
    player_decks = defaultdict(set)
    # I'm hard-coding seeding of win_cons and formats (in `app/sql/__init__.py`), rather than requiring them to be
    # manually seeded - but this would be where we'd track them if we wanted them to be seeded
    # win_types = set()
    # formats = set()

    for row_idx, row in enumerate(reader):
        if not row:
            continue
        for i in range(6):
            player_id = f"Player {i+1}"
            if row[player_id]:
                player_decks[row[player_id]].add(row[f"Deck {i+1}"])
            # Hack because of missing data in the original spreadsheet... :)
            if row_idx == 28 and i == 3:
                print("In the suspect row")
                player_decks["stranger"].add(row["Deck 4"])

        # See above
        # win_types.add(row['Type of win'])
        # formats.add(row['Format'])

    # If we cared about memory efficiency we could have instead made `player_decks` into an extensible data structure
    # and added this information in there, but I'm hardly going to be dealing with memory-intensive amounts of
    # data in this app.
    player_id_lookup = {}
    deck_id_lookup = {}

    for player_name, decks in player_decks.items():
        player = crud.create_player(
            db=db, player=schemas.PlayerCreate(name=player_name)
        )
        LOGGER.info(f"Seeded {player=}")
        player_id = player.id
        player_id_lookup[player_name] = player_id
        for deck_name in decks:
            deck = crud.create_deck(
                db=db,
                deck=schemas.DeckCreate(
                    name=deck_name, description="", owner_id=player_id
                ),
            )
            LOGGER.info(f"Seeded {deck=}")
            deck_id_lookup[deck_name] = deck.id

    def parse_date(date_string) -> datetime.datetime:
        month, day, year = date_string.split("/")
        return datetime.datetime.strptime(
            f"{year}-{month.rjust(2, '0')}-{day.rjust(2, '0')}", "%y-%m-%d"
        )

    win_types = db.query(WinType).all()
    formats = db.query(Format).all()

    # Recreate the reader to consume the rows again.
    # (Again, if we _really_ cared about efficiency we could have stored this data on the first pass to avoid a
    # retraversal. I suspect that the overhead of O(2*n) vs. O(n) data-reads is going to be insignificant)
    # ((Yes, I know that's an abuse of Big-O notation, shut up - you knew what I meant :P ))
    reader = csv.DictReader(file_contents, delimiter=",")
    for row in reader:
        # Note that we intentionally create via the API, not via direct `crud.create_game`, to trigger ELO calculation.

        created_game = create_game(
            schemas.GameCreate(
                date=parse_date(row["Date"]),
                **{
                    f"deck_id_{i+1}": deck_id_lookup[row[f"Deck {i+1}"]]
                    for i in range(6)
                    if row[f"Deck {i+1}"]
                },
                winning_deck_id=deck_id_lookup[row["Winning Deck"]],
                number_of_turns=int(row["# turns"]),
                first_player_out_turn=row["turn 1st player out"],
                win_type_id=[
                    win_type.id
                    for win_type in win_types
                    if win_type.name == row["Type of win"]
                ][0],
                format_id=[
                    format.id for format in formats if format.name == row["Format"]
                ][0],
                description=row["Notes"],
            ),
            db,
        )
        LOGGER.info(f"Seeded {created_game=}")

    return "Ok!"


@html_router.get("/")
def main(request: Request, db=Depends(get_db)):
    return jinja_templates.TemplateResponse(
        request,
        "/seed.html",
    )
