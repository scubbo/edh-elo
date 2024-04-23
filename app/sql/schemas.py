from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int

    model_config = {"from_attributes": True}


class DeckBase(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: int


class DeckCreate(DeckBase):
    pass


class Deck(DeckBase):
    id: int

    model_config = {"from_attributes": True}


class WinTypeBase(BaseModel):
    name: str


class WinTypeCreate(WinTypeBase):
    pass


class WinType(WinTypeBase):
    id: int

    model_config = {"from_attributes": True}


class GameBase(BaseModel):
    date: datetime
    deck_id_1: int
    deck_id_2: int
    deck_id_3: Optional[int] = None
    deck_id_4: Optional[int] = None
    deck_id_5: Optional[int] = None
    deck_id_6: Optional[int] = None
    winning_deck_id: int
    number_of_turns: int
    first_player_out_turn: int
    win_type_id: int
    format_id: int
    description: str


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int

    model_config = {"from_attributes": True}


# No need for an EloScoreBase because this will never be created via API - it's only ever calculated internally.
class EloScore(BaseModel):
    id: int
    after_game_id: int
    on_date: datetime
    deck_id: int
    score: float
