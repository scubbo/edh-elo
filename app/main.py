from flask import Blueprint, request
from . import db
from .models import Deck, Game, Player

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return 'Hello, World - but new!'

@main.route("/player", methods=["POST"])
def create_player():
    data = request.json
    player = Player(
        name=data['name']
    )
    db.session.add(player)
    db.session.commit()
    return {'id': player.id}

# TODO - implement a GET method - can it be a separate method, or must it be the same annotation with an `if method==`?
# Time for testing, methinks!
