from sqlalchemy.orm import Session

from . import models, schemas


def get_player_by_id(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()


def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Player).offset(skip).limit(limit).all()


def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def delete_player_by_id(db: Session, player_id: int):
    db.query(models.Player).filter(models.Player.id == player_id).delete()
    db.commit()


def get_deck_by_id(db: Session, deck_id: int):
    return db.query(models.Deck).filter(models.Deck.id == deck_id).first()


def get_decks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Deck).offset(skip).limit(limit).all()


def create_deck(db: Session, deck: schemas.DeckCreate):
    db_deck = models.Deck(**deck.model_dump())
    db.add(db_deck)
    db.commit()
    db.refresh(db_deck)
    return db_deck


def delete_deck_by_id(db: Session, deck_id: int):
    db.query(models.Deck).filter(models.Deck.id == deck_id).delete()
    db.commit()
    return "", 204
