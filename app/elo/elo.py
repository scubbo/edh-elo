from typing import Iterable, List

K_FACTOR = 10.0
BETA = 200


def rerank(ratings: List[float], winning_player_idx: int) -> Iterable[float]:
    expectations = _expectations(ratings)
    return [
        float(rating)
        + (K_FACTOR * ((1.0 if winning_player_idx == idx else 0.0) - expectations[idx]))
        for idx, rating in enumerate(ratings)
    ]


def _expectations(ratings: List[float]) -> List[float]:
    return [
        _calculate_expectation(rating, ratings[:idx] + ratings[idx + 1 :])
        for idx, rating in enumerate(ratings)
    ]


def _calculate_expectation(rating: float, other_ratings: List[float]) -> float:
    return sum(
        [_pairwise_expectation(rating, other_rating) for other_rating in other_ratings]
    ) / (float(len(other_ratings) + 1) * len(other_ratings) / 2)


def _pairwise_expectation(rating: float, other_rating: float) -> float:
    """
    Gives the expected score of `rating` against `other_rating`
    """
    diff = float(other_rating) - float(rating)
    f_factor = 2 * BETA  # rating disparity
    ret_val = 1.0 / (1 + 10 ** (diff / f_factor))
    return ret_val
