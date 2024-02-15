from . import models
from .database import SessionLocal


def prime_database():
    db = SessionLocal()
    win_types = db.query(models.WinType).all()
    if not win_types:
        db.add(models.WinType(name="Combat Damage"))
        db.add(models.WinType(name="Commander Damage"))
        db.add(models.WinType(name="Direct Damage"))
        db.add(models.WinType(name="Poison"))
        db.add(models.WinType(name="Decking"))
        db.add(models.WinType(name="other"))
        db.commit()
