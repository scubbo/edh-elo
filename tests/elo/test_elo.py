from typing import Iterable

from app.elo import rerank


def test():
    # From https://github.com/sublee/elo/blob/master/elotests.py
    assert _almost_equal(rerank([1200, 800], 1), [1190.909, 809.091])
    # Couldn't find any test-cases for multiplayer games.


def _almost_equal(actual: Iterable, expected: Iterable) -> bool:
    assert len(actual) == len(expected)
    for f, s in zip(actual, expected):
        if (s - f) > (0.00001 * f):
            return False
    else:
        return True
