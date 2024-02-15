from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    decks = relationship("Deck", back_populates="owner")


class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("players.id"))

    owner = relationship("Player", back_populates="decks")


class WinType(Base):
    __tablename__ = "wintypes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    deck_id_1 = Column(Integer, ForeignKey("decks.id"), nullable=False)
    deck_id_2 = Column(Integer, ForeignKey("decks.id"), nullable=False)
    deck_id_3 = Column(Integer, ForeignKey("decks.id"))
    deck_id_4 = Column(Integer, ForeignKey("decks.id"))
    deck_id_5 = Column(Integer, ForeignKey("decks.id"))
    deck_id_6 = Column(Integer, ForeignKey("decks.id"))
    winning_deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False)
    number_of_turns = Column(Integer, nullable=False)
    first_player_out_turn = Column(Integer, nullable=False)
    win_type_id = Column(Integer, ForeignKey("wintypes.id"), nullable=False)
    description = Column(String)
