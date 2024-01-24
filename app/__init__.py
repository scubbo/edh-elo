import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        sys.stderr.write("YOU NEED TO SET AN ENV VARIABLE NAMED SECRET_KEY\n")
        sys.exit(1)
    app.config["SECRET_KEY"] = secret_key

    # TODO - support other database types 🙃
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URI", "sqlite:///db.sqlite"
    )

    db.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # TODO - understand how this works, since `db.create_all()` requires that the model classes have already been
    # imported in order to know what to create. Perhaps `__init__.py` just magically has the context of everything in
    # its module? Good opportunity to learn more about the Python import system!
    with app.app_context():
        db.create_all()

    return app
