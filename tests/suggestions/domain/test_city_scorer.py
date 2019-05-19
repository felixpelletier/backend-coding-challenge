import pytest

from tests.suggestions.city_infos import city_infos_provider_fakes
from tests.suggestions.domain import city_scorer_fakes
from src.suggestions.domain import city_scorer
from src.suggestions.service import CitySuggestionsQuery

SOME_FAKE_CITY = city_infos_provider_fakes.generate_fake_city_infos()
SOME_QUERY = CitySuggestionsQuery(query="Unimportant query")


@pytest.fixture
def default_city_scorer():
    return city_scorer.CityScorer()


def test_given_no_metrics_city_has_score_of_zero(default_city_scorer):
    score = default_city_scorer.compute_score_for_city(SOME_FAKE_CITY, SOME_QUERY)

    assert score == 0


def test_given_one_metric_with_a_nonzero_weight_then_its_score_is_the_city_score(default_city_scorer):
    expected_score = 0.5
    some_nonzero_weight = 0.34
    metric = city_scorer_fakes.FakeSuggestionMetric(expected_score)
    default_city_scorer.add_metric(metric, some_nonzero_weight)

    score = default_city_scorer.compute_score_for_city(SOME_FAKE_CITY, SOME_QUERY)

    assert score == expected_score


def test_given_multiple_metrics_with_a_nonzero_weight_then_its_score_the_weighed_sum_of_all_metrics(default_city_scorer):
    expected_score = 0.5
    metric1 = city_scorer_fakes.FakeSuggestionMetric(0.2)
    metric2 = city_scorer_fakes.FakeSuggestionMetric(0.4)
    metric3 = city_scorer_fakes.FakeSuggestionMetric(0.8)
    default_city_scorer.add_metric(metric1, 4)
    default_city_scorer.add_metric(metric2, 12)
    default_city_scorer.add_metric(metric3, 8)

    score = default_city_scorer.compute_score_for_city(SOME_FAKE_CITY, SOME_QUERY)

    assert pytest.approx(expected_score) == score
