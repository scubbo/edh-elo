import os
import pathlib
import pytest

# TODO - this seems to be a "magic path" which makes fixtures available. Learn more about it by reading
# https://stackoverflow.com/questions/34466027/what-is-conftest-py-for-in-pytest

from app import create_app

# https://flask.palletsprojects.com/en/2.3.x/testing/


@pytest.fixture()
def app_fixture():
    # Start afresh!
    test_database_name = "testing-db.sqlite"
    database_location = pathlib.Path("instance").joinpath(test_database_name)
    if database_location.exists():
        database_location.unlink()

    os.environ["DATABASE_URI"] = f"sqlite:///{test_database_name}"
    os.environ["SECRET_KEY"] = "testing-secret-key"

    app = create_app()
    # app.config.update({
    #     'TESTING': True
    # })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app_fixture):
    return app_fixture.test_client()


@pytest.fixture()
def runner(app_fixture):
    return app_fixture.test_cli_runner()
