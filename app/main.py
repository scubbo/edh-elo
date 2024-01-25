from flask import Blueprint, render_template, request
from . import db
from .models import Deck, Player

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Main Page
    ---
    responses:
      200:
        description: A friendly greeting
        schema:
          type: string
    """
    return "Hello, World - but new!"


@main.route("/player", methods=["POST"])
def create_player():
    """Create a Player
    ---
    requestBody:
      description: Payload describing the player
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                example: Jim Bloggs
            required:
              - name
    responses:
      201:
        description: Payload containing Player Id
        schema:
          type: object
          properties:
            id:
              type: number
          required:
            - id
    tags:
      - player
    """
    data = request.json
    player = Player(name=data["name"])
    db.session.add(player)
    db.session.commit()
    return {"id": player.id}, 201


@main.route("/player/<player_id>")
def get_player(player_id: str):
    """Get a Player
    ---
    parameters:
      - name: player_id
        in: path
        required: true
        schema:
          type: integer
          minimum: 1
        description: The Player Id
    requestBody:
      content:
        application/json:
          schema: {}
        text/html:
          schema: {}
    responses:
      200:
        description: Payload describing player
        content:
          application/json:
            schema:
              id: Player
          text/html:
            schema:
              type: string
      404:
        description: Player not found
        content:
            application/json: {}
            text/html: {}
    tags:
      - player
    """
    # TODO - actually, the schema above doesn't reference the `Player` class as I'd hoped it would.
    # The docs at https://github.com/flasgger/flasgger#extracting-definitions are not super-clear.
    # _Maybe_ what I'm trying to do is not possible?
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
    """Delete a Player
    ---
    parameters:
      - name: player_id
        in: path
        required: true
        schema:
          type: integer
          minimum: 1
        description: The Player Id
    requestBody:
      content:
        application/json:
          schema: {}
    responses:
      204:
        description: Empty
        content:
          application/json:
            schema: {}
    tags:
      - player
    """
    # Note - no checking that the player exists, because HTTP semantics specify
    # that `DELETE` should be idempotent.
    db.session.query(Player).filter(Player.id == int(player_id)).delete()
    db.session.commit()
    return "", 204


@main.route("/deck", methods=["POST"])
def create_deck():
    """Create a Deck
    ---
    requestBody:
      description: Payload describing the deck
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                example: My First Deck
              description:
                type: string
                example: Better than yours!
              owner_id:
                type: number
                example: 1
            required:
              - name
              - owner_id
    responses:
      201:
        description: Payload containing Deck Id
        schema:
          type: object
          properties:
            id:
              type: number
          required:
            - id
      400:
        description: Owner not found
    tags:
      - deck
    """
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
    return {"id": deck.id}, 201


@main.route("/deck/<deck_id>")
def get_deck(deck_id: str):
    """Get a Deck
    ---
    parameters:
      - name: deck_id
        in: path
        required: true
        schema:
          type: integer
          minimum: 1
        description: The Deck Id
    requestBody:
      content:
        application/json:
          schema: {}
        text/html:
          schema: {}
    responses:
      200:
        description: Payload describing deck
        content:
          application/json:
            schema:
              id: Deck
          text/html:
            schema:
              type: string
      404:
        description: Deck not found
        content:
            application/json: {}
            text/html: {}
    tags:
      - deck
    """
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
    """Delete a Deck
    ---
    parameters:
      - name: deck_id
        in: path
        required: true
        schema:
          type: integer
          minimum: 1
        description: The Deck Id
    requestBody:
      content:
        application/json:
          schema: {}
    responses:
      204:
        description: Empty
        content:
          application/json:
            schema: {}
    tags:
      - deck
    """
    db.session.query(Deck).filter(Deck.id == int(deck_id)).delete()
    db.session.commit()
    return "", 204


# TODO - would this be better as a method on a class extending `db.Model` that the classes in `models.py` could then
# extend?
# (Probably not, as we'd still need to explicitly call it - it wouldn't be implicitly called _by_ Flask)
def _jsonify(o):
    return {k: v for (k, v) in o.__dict__.items() if k != "_sa_instance_state"}
