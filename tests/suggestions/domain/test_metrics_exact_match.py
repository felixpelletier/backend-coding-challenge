
import pytest

from src.suggestions.domain import metrics

from tests.suggestions.domain.metrics_test_helpers import get_score_from_city_name_metric
from tests.suggestions.domain.metrics_test_helpers import get_score_from_alt_city_name_metric

A_CITY_NAME = "London"
A_DIFFERENT_CITY_NAME = "Prague"

@pytest.fixture
def exact_match_metric():
    return metrics.ExactNameMatchMetric()


def test_when_query_is_exactly_the_city_name_score_one(exact_match_metric):
    assert 1.0 == get_score_from_city_name_metric(exact_match_metric, A_CITY_NAME, A_CITY_NAME)


def test_when_query_is_exactly_at_least_one_of_the_alternative_city_names_score_one(exact_match_metric):
    assert 1.0 == get_score_from_alt_city_name_metric(exact_match_metric, A_CITY_NAME, A_CITY_NAME)


def test_match_is_case_insensitive(exact_match_metric):
    assert 1.0 == get_score_from_alt_city_name_metric(exact_match_metric, A_CITY_NAME.upper(), A_CITY_NAME.lower())


def test_when_query_different_from_city_name_score_none(exact_match_metric):
    assert get_score_from_city_name_metric(exact_match_metric, A_CITY_NAME, A_DIFFERENT_CITY_NAME) is None
