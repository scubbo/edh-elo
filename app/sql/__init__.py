from . import models
from .database import SessionLocal


def prime_database():
    db = SessionLocal()
    win_types = db.query(models.WinType).all()
    if not win_types:
        db.add(models.WinType(name="combat damage"))
        db.add(models.WinType(name="21+ commander"))
        db.add(models.WinType(name="aristocrats/burn"))
        db.add(models.WinType(name="poison"))
        db.add(models.WinType(name="quality of life concede"))
        db.add(models.WinType(name="alt win-con"))
        db.add(models.WinType(name="mill"))
        db.commit()

    formats = db.query(models.Format).all()
    if not formats:
        db.add(models.Format(name="FFA"))
        db.add(models.Format(name="Star"))
        db.commit()
