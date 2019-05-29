"""

This module is not a full test of the Levenshtein distance algorithm.
It is intended as a regression test in case the implementation changes.

"""
import pytest

from src.suggestions.scoring import metrics

from tests.suggestions.scoring.metrics.metrics_test_helpers import get_score_from_city_name_metric
from tests.suggestions.scoring.metrics.metrics_test_helpers import get_score_from_alt_city_name_metric

TEST_DATA = [
    ("Quebec", "Quebec", 0),        # Strings exactly equal have distance of 0
    ("Quebec", "quebec", 0),        # And this is case insensitive
    ("Quebec", "Qubec", 1),         # Letter insertion has distance of 1
    ("Quebec", "Quebe", 1),         # Anywhere in the word
    ("Quebec", "", 6),              # Even with no letters at all
    ("Canada", "Caaaanada", 3),     # Letter deletion has distance of 1
    ("Canada", "Cenada", 2),        # Letter replacement has distance of 2
    ("Quebec", "London", 12),       # Therefore, all different characters have distance equal to sum of lengths
    ("Lindström", "Lindstrom", 1),  # Unicode character are supported. Accented characters count as an addition.
]


@pytest.fixture
def levenshtein_metric():
    return metrics.LevenshteinCityNameSimilarityMetric()


def compute_expected_score_from_levenshtein_distance(word1, word2, distance):
    length_sum = len(word1) + len(word2)
    return 1.0 - (distance / length_sum)


@pytest.mark.parametrize("data", TEST_DATA)
def test_compute_score(levenshtein_metric, data):
    city_name, partial_name, levenshtein_distance = data
    expected_score = compute_expected_score_from_levenshtein_distance(
        word1=city_name, word2=partial_name,
        distance=levenshtein_distance
    )

    actual_score = get_score_from_city_name_metric(levenshtein_metric, city_name, partial_name)
    assert actual_score == pytest.approx(expected_score, rel=0.01)


def test_compute_score_for_alt_city_name_gives_best_score_of_all_names(levenshtein_metric):
    partial_name = "Qubec"
    best_alt_name = "Quebec"
    expected_score = compute_expected_score_from_levenshtein_distance(best_alt_name, partial_name, 1)
    alt_city_names = ["London", "Canada"] + [best_alt_name] + ["SOME other name"]

    actual_score = get_score_from_alt_city_name_metric(levenshtein_metric, alt_city_names, partial_name)
    assert actual_score == pytest.approx(expected_score, rel=0.01)


