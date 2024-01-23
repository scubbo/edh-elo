from . import db

# Note that a `Player` is "someone who plays in the Pod", whereas `User` (which will be implemented later) is "a user of
# this system". While all Users will _probably_ be Players, they do not have to be - and, it is likely that several
# Players will not be Users (if they don't register to use the system).
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String)
    owner = db.Column(db.String, db.ForeignKey(Player.__table__.c.id), nullable=False, )

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO - columns like `location`, `writeups`, etc.

    # Not wild about this structure ("fill in non-null columns to indicate decks that were present"), but what can you
    # do with a database that doesn't support arrays? (Postgres _does_, but I don't wanna ramp up on a whole other
    # database system just for that...)
    deck_1 = db.Column(db.Integer)
    deck_2 = db.Column(db.Integer)
    deck_3 = db.Column(db.Integer)
    deck_4 = db.Column(db.Integer)
    deck_5 = db.Column(db.Integer)
    deck_6 = db.Column(db.Integer)
    deck_7 = db.Column(db.Integer)
    deck_8 = db.Column(db.Integer)
    deck_9 = db.Column(db.Integer)
    deck_10 = db.Column(db.Integer)
