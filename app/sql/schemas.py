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
