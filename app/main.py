from flask import Blueprint, render_template, request
from . import db
from .models import Deck, Player

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


@main.route("/player/<player_id>", methods=["DELETE"])
def delete_player(player_id: str):
    # Note - no checking that the player exists, because HTTP semantics specify
    # that `DELETE` should be idempotent.
    db.session.query(Player).filter(Player.id == int(player_id)).delete()
    db.session.commit()
    return "", 204


@main.route("/deck", methods=["POST"])
def create_deck():
    data = request.json
    owner_id = data["owner_id"]

    player_from_db = db.session.get(Player, int(owner_id))
    if not player_from_db:
        return f"Owner id {owner_id} not found", 400

    deck = Deck(
        name=data["name"], description=data.get("description"), owner_id=owner_id
    )
    db.session.add(deck)
    db.session.commit()
    print("Finished creating the deck!")
    return {"id": deck.id}


@main.route("/deck/<deck_id>")
def get_deck(deck_id: str):
    deck_from_db = db.session.get(Deck, int(deck_id))
    if not deck_from_db:
        return "Not Found", 404

    deck_data = _jsonify(deck_from_db)

    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        return deck_data
    else:  # Assume they want HTML
        owner_data = db.session.get(Player, int(deck_data["owner_id"]))
        return render_template(
            "deck_detail.html", deck=deck_data, owner=_jsonify(owner_data)
        )


@main.route("/deck/<deck_id>", methods=["DELETE"])
def delete_deck(deck_id: str):
    db.session.query(Deck).filter(Deck.id == int(deck_id)).delete()
    db.session.commit()
    return "", 204


# TODO - would this be better as a method on a class extending `db.Model` that the classes in `models.py` could then
# extend?
# (Probably not, as we'd still need to explicitly call it - it wouldn't be implicitly called _by_ Flask)
def _jsonify(o):
    return {k: v for (k, v) in o.__dict__.items() if k != "_sa_instance_state"}
