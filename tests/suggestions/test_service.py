import pytest

from src.suggestions import service

from tests.suggestions.city_infos import city_infos_provider_fakes
from tests.suggestions.scoring import city_scorer_fakes

SOME_HIGH_CITY_COUNT = 100
SOME_NON_EMPTY_PARTIAL_CITY_NAME = "Quebe"

SOME_CITY_NAME = "Quebec"
SOME_CITY_SCORE = 0.1

SOME_OTHER_CITY_NAME = "Ottawa"
SOME_OTHER_CITY_SCORE = 0.4

SOME_LONGITUDE = 2.4
SOME_LATITUDE = -32.6

SOME_OTHER_LONGITUDE = -25.4
SOME_OTHER_LATITUDE = 55.5


def construct_query_from_dict(query_dict):
    return service.CitySuggestionsQuery(
        partial_name=query_dict.get('q'),
        longitude=query_dict.get("longitude", None),
        latitude=query_dict.get("latitude", None),
    )


@pytest.fixture
def fake_city_infos_provider():
    return city_infos_provider_fakes.FakeCityInfosProvider()


@pytest.fixture
def fake_city_scorer():
    return city_scorer_fakes.FakeCityScorer()


@pytest.fixture
def default_service(fake_city_infos_provider, fake_city_scorer):
    return service.CitySuggestionsService(fake_city_infos_provider, fake_city_scorer)


def test_given_empty_query_return_no_suggestions(default_service, fake_city_infos_provider):
    fake_city_infos_provider.fill_with_random_data(SOME_HIGH_CITY_COUNT)
    query = construct_query_from_dict({'q': ""})

    response = default_service.get_suggestions(query)

    assert len(response.suggestions) == 0


def test_given_nonempty_query_and_enough_cities_return_at_least_one_suggestion(default_service,
                                                                               fake_city_infos_provider):
    fake_city_infos_provider.fill_with_random_data(SOME_HIGH_CITY_COUNT)
    query = construct_query_from_dict({'q': SOME_NON_EMPTY_PARTIAL_CITY_NAME})

    response = default_service.get_suggestions(query)

    assert len(response.suggestions) != 0


def test_given_nonempty_query_and_enough_cities_return_five_suggestions(default_service,
                                                                        fake_city_infos_provider):
    fake_city_infos_provider.fill_with_random_data(SOME_HIGH_CITY_COUNT)
    query = construct_query_from_dict({'q': SOME_NON_EMPTY_PARTIAL_CITY_NAME})

    response = default_service.get_suggestions(query)

    assert len(response.suggestions) == 5


def test_given_a_scorer_when_asking_suggestions_scores_are_computed_by_scorer(default_service,
                                                                              fake_city_infos_provider,
                                                                              fake_city_scorer):
    fake_city_infos_provider.add_city_infos({"name": SOME_CITY_NAME})
    fake_city_scorer.set_score_for_city(SOME_CITY_NAME, SOME_CITY_SCORE)

    fake_city_infos_provider.add_city_infos({"name": SOME_OTHER_CITY_NAME})
    fake_city_scorer.set_score_for_city(SOME_OTHER_CITY_NAME, SOME_OTHER_CITY_SCORE)

    query = construct_query_from_dict({'q': SOME_NON_EMPTY_PARTIAL_CITY_NAME})

    response = default_service.get_suggestions(query)

    assert any(city_suggestion.name == SOME_CITY_NAME and city_suggestion.score == SOME_CITY_SCORE
               for city_suggestion in response.suggestions)
    assert any(city_suggestion.name == SOME_OTHER_CITY_NAME and city_suggestion.score == SOME_OTHER_CITY_SCORE
               for city_suggestion in response.suggestions)


def test_given_some_cities_when_asking_suggestions_city_coordinates_are_taken_from_city_info_provider(default_service,
                                                                                                      fake_city_infos_provider):
    fake_city_infos_provider.add_city_infos({
        "name": SOME_CITY_NAME,
        "coordinates": {
            "lat": SOME_LATITUDE,
            "long": SOME_LONGITUDE,
        },
    })
    fake_city_infos_provider.add_city_infos({
        "name": SOME_OTHER_CITY_NAME,
        "coordinates": {
            "lat": SOME_OTHER_LATITUDE,
            "long": SOME_OTHER_LONGITUDE,
        },
    })
    query = construct_query_from_dict({'q': SOME_NON_EMPTY_PARTIAL_CITY_NAME})

    response = default_service.get_suggestions(query)

    assert any(city_suggestion.name == SOME_CITY_NAME
               and city_suggestion.latitude == SOME_LATITUDE
               and city_suggestion.longitude == SOME_LONGITUDE
               for city_suggestion in response.suggestions)
    assert any(city_suggestion.name == SOME_OTHER_CITY_NAME
               and city_suggestion.latitude == SOME_OTHER_LATITUDE
               and city_suggestion.longitude == SOME_OTHER_LONGITUDE
               for city_suggestion in response.suggestions)
