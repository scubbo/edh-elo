from typing import Iterable

K_FACTOR = 10
BETA = 200


def rerank(ratings: Iterable[int], winning_player_idx: int) -> Iterable[int]:
    expectations = _expectations(ratings)
    return [
        rating
        + (K_FACTOR * ((1 if winning_player_idx == idx else 0) - expectations[idx]))
        for idx, rating in enumerate(ratings)
    ]


def _expectations(ratings: Iterable[int]) -> Iterable[int]:
    return [
        _calculate_expectation(rating, ratings[:idx] + ratings[idx + 1 :])
        for idx, rating in enumerate(ratings)
    ]


def _calculate_expectation(rating: int, other_ratings: Iterable[int]) -> int:
    return sum(
        [_pairwise_expectation(rating, other_rating) for other_rating in other_ratings]
    ) / (float(len(other_ratings) + 1) * len(other_ratings) / 2)


def _pairwise_expectation(rating: int, other_rating: int) -> Iterable[int]:
    """
    Gives the expected score of `rating` against `other_rating`
    """
    diff = float(other_rating) - float(rating)
    f_factor = 2 * BETA  # rating disparity
    return 1.0 / (1 + 10 ** (diff / f_factor))
