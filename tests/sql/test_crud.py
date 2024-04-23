import pathlib
import pytest
import random
import string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.sql.models import Base
from app.sql import crud
from app.sql import schemas


def test_create_player(isolated_database):
    # No risk of interference because the fixture has `scope="function"`,
    # so creates a new database for every invocation!
    _test_create_and_retrieve(isolated_database, "Timmy")
    # Note there's no need to cleanup this database because the fixture takes care of it for us!


def test_parallel(isolated_database):
    _test_create_and_retrieve(isolated_database, "Johnny")


def test_more_parallelization(isolated_database):
    _test_create_and_retrieve(isolated_database, "Spike")


def _test_create_and_retrieve(db, name: str):
    empty_get_player = crud.get_player_by_id(db, 1)
    assert empty_get_player is None

    create_response = crud.create_player(db, schemas.PlayerCreate(name=name))
    assert create_response.id == 1
    assert create_response.name == name

    get_player = crud.get_player_by_id(db, 1)
    assert get_player.name == name


@pytest.fixture(scope="function")
def isolated_database(request, cleanups):
    database_dir = "database"
    db_dir_path = pathlib.Path(database_dir)
    if not db_dir_path.exists():
        db_dir_path.mkdir()
    db_dir_path.chmod(0o777)

    isolated_db_name = f"isolated_database_{''.join([random.choice(string.ascii_lowercase) for _ in range(5)])}.db"
    isolated_db_path = db_dir_path.joinpath(isolated_db_name)

    engine = create_engine(f"sqlite:///{isolated_db_path.absolute()}")

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def success_cleanup():
        isolated_db_path.unlink()

    def failure_cleanup():
        print(
            f"Isolated database {isolated_db_path.absolute()}, used in test `{request.node.name}` at path `{request.node.path.absolute()}`, has been preserved for debugging"
        )

    cleanups.add_success(success_cleanup)
    cleanups.add_failure(failure_cleanup)

    yield SessionLocal()
    # yield isolated_db_path
