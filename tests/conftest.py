import os
import pathlib
import pytest

from fastapi.testclient import TestClient


def prime_database():
    # Start afresh!
    database_dir = "database"
    db_dir_path = pathlib.Path(database_dir)
    if not db_dir_path.exists():
        db_dir_path.mkdir()
    db_dir_path.chmod(0o777)

    test_database_name = "testing_database.db"
    db_path = db_dir_path.joinpath(test_database_name)

    if db_path.exists():
        db_path.unlink()

    print(f"Setting database_url using {db_path}")
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"


prime_database()

# This must be after `prime_database`, as the database initialization will happen
# during the import, and must do so after the environment-var setting
from app import app  # noqa: E402


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)
