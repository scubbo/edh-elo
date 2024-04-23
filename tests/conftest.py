import os
import pathlib
import pytest

from typing import Callable

from fastapi.testclient import TestClient


# https://stackoverflow.com/questions/69281822/how-to-only-run-a-pytest-fixture-cleanup-on-test-error-or-failure,
# Though syntax appears to have changed
# https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    # TODO - we may care about more than just a binary result!
    # (i.e. a skipped test is neither passed nor failed...probably?)
    setattr(
        item,
        "rep_" + outcome.get_result().when + "_passed",
        outcome.get_result().passed,
    )


class Cleanups(object):
    def __init__(self):
        self.success_cleanups = []
        self.failure_cleanups = []

    def add_success(self, success_cleanup: Callable[[], None]):
        self.success_cleanups.append(success_cleanup)

    def add_failure(self, failure_cleanup: Callable[[], None]):
        self.failure_cleanups.append(failure_cleanup)


@pytest.fixture
def cleanups(request):
    cleanups = Cleanups()
    yield cleanups

    if request.node.rep_call_passed:
        cleanups = cleanups.success_cleanups
    else:
        cleanups = cleanups.failure_cleanups
    if cleanups:
        for cleanup in cleanups[::-1]:  # Apply in reverse order
            cleanup()


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
