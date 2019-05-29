
import math
import pytest

from src.suggestions.scoring import metrics

from tests.suggestions.scoring.metrics.metrics_test_helpers import get_score_from_population_metric

WORLD_POPULATION = 8000000000
A_HIGHLY_POPULATED_CITY = 100000
A_MILDLY_POPULATED_CITY = 1000
A_LOWLY_POPULATED_CITY = 10


@pytest.fixture
def log_population_metric():
    return metrics.LogarithmicPopulationMetric()


def test_when_population_is_really_high_then_score_one(log_population_metric):
    assert 1.0 == get_score_from_population_metric(log_population_metric, WORLD_POPULATION)


def test_when_population_is_zero_score_is_zero(log_population_metric):
    assert 0.0 == get_score_from_population_metric(log_population_metric, 0)


def test_score_varies_logarithmically(log_population_metric):
    score_mildly_populated_city = get_score_from_population_metric(log_population_metric, A_MILDLY_POPULATED_CITY)
    log_mildly_populated_city = math.log10(A_MILDLY_POPULATED_CITY)
    multiplier = score_mildly_populated_city / log_mildly_populated_city

    log_lowly_populated_city = math.log10(A_LOWLY_POPULATED_CITY)
    expected_score = log_lowly_populated_city * multiplier

    score_lowly_populated_city = get_score_from_population_metric(log_population_metric, A_LOWLY_POPULATED_CITY)
    assert score_lowly_populated_city == expected_score
