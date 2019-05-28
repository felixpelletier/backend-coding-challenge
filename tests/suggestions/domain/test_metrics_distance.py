
import pytest

from src.suggestions.domain import metrics

from tests.suggestions.domain.metrics_test_helpers import get_score_from_coordinates_metric

VERY_DISTANT_CITY_PAIR = ((-32.57, -60.40), (32.93, 119.83))
EXACT_LOCATION_CITY_PAIR = ((-32.57, -60.40), (-32.57, -60.40))
DISTANCE_OF_300KM_CITY_PAIRS = ((46.8139, -71.2080), (45.6, -74.6))
DISTANCE_OF_1000KM_CITY_PAIRS = ((46.8139, -71.2080), (38.9872, -77.0369))


@pytest.fixture
def distance_metric():
    return metrics.HaversineLocationDistanceMetric()


def get_score(metric, city_pair):
    city_coordinates, query_coordinates = city_pair
    return get_score_from_coordinates_metric(metric, city_coordinates, query_coordinates)


def assert_score_is_correct(distance_metric, expected_score, city_pair):
    assert get_score(distance_metric, city_pair) == pytest.approx(expected_score, abs=0.02, rel=0.02)


def test_when_at_exact_location_score_is_one(distance_metric):
    assert_score_is_correct(distance_metric, 1.0, EXACT_LOCATION_CITY_PAIR)


def test_when_very_far_score_is_zero(distance_metric):
    assert_score_is_correct(distance_metric, 0.0, VERY_DISTANT_CITY_PAIR)


def test_at_300km(distance_metric):
    assert_score_is_correct(distance_metric, 0.83, DISTANCE_OF_300KM_CITY_PAIRS)


def test_at_1000km(distance_metric):
    assert_score_is_correct(distance_metric, 0.14, DISTANCE_OF_1000KM_CITY_PAIRS)
