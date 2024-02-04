from typing import List, Optional
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
    deck_id_1: int
    deck_id_2: int
    deck_id_3: int
    deck_id_4: int
    deck_id_5: int
    deck_id_6: int
    winning_deck_id: int
    number_of_turns: int
    first_player_out_turn: int
    win_type_id: int
    description: str


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int

    model_config = {"from_attributes": True}
