from flask import Blueprint, render_template, request
from . import db
from .models import Deck, Game, Player

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return "Hello, World - but new!"


@main.route("/player", methods=["POST"])
def create_player():
    data = request.json
    player = Player(name=data["name"])
    db.session.add(player)
    db.session.commit()
    return {"id": player.id}


@main.route("/player/<player_id>")
def get_player(player_id: str):
    player_from_db = db.session.get(Player, int(player_id))
    if not player_from_db:
        return "Not Found", 404

    player_data = _jsonify(player_from_db)

    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        return player_data
    else:  # Assume they want HTML
        return render_template("player_detail.html", **player_data)


# TODO - implement a GET method - can it be a separate method, or must it be the same annotation with an `if method==`?
# Time for testing, methinks!


# TODO - would this be better as a method on a class extending `db.Model` that the classes in `models.py` could then
# extend?
# (Probably not, as we'd still need to explicitly call it - it wouldn't be implicitly called _by_ Flask)
def _jsonify(o):
    return {k: v for (k, v) in o.__dict__.items() if k != "_sa_instance_state"}
