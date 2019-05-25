
import pytest

from src.suggestions.domain import metrics

from tests.suggestions.domain.metrics_test_helpers import get_score_from_city_name_metric
from tests.suggestions.domain.metrics_test_helpers import get_score_from_alt_city_name_metric

A_CITY_NAME = "London"
A_CITY_NAME_MISSING_LAST_LETTER = "Londo"
FIRST_LETTER_OF_A_CITY_NAME = "L"
A_DIFFERENT_CITY_NAME = "Prague"

@pytest.fixture
def starts_with_metric():
    return metrics.NameStartsWithMetric()


def test_when_query_is_exactly_the_city_name_score_one(starts_with_metric):
    assert 1.0 == get_score_from_city_name_metric(starts_with_metric, A_CITY_NAME, A_CITY_NAME)


def test_when_query_is_exactly_at_least_one_of_the_alternative_city_names_score_one(starts_with_metric):
    assert 1.0 == get_score_from_alt_city_name_metric(starts_with_metric, A_CITY_NAME, A_CITY_NAME)


def test_when_query_is_the_city_without_last_letter_score_one(starts_with_metric):
    assert 1.0 == get_score_from_city_name_metric(starts_with_metric, A_CITY_NAME, A_CITY_NAME_MISSING_LAST_LETTER)


def test_when_query_is_the_first_lette_of_the_city_name_score_one(starts_with_metric):
    assert 1.0 == get_score_from_alt_city_name_metric(starts_with_metric, A_CITY_NAME, FIRST_LETTER_OF_A_CITY_NAME)


def test_when_query_different_from_city_name_score_none(starts_with_metric):
    assert get_score_from_city_name_metric(starts_with_metric, A_CITY_NAME, A_DIFFERENT_CITY_NAME) is None
