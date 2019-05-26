
from typing import Tuple, List

from src.suggestions.domain import city_scorer
from src.suggestions import service
from src.suggestions.city_infos import provider_interface

IRRELEVANT_CITY_NAME = "Irrelevant and long enough so it clashes with nothing else"
IRRELEVANT_CITY_COORDINATES = provider_interface.CityCoordinates(0, 0)
IRRELEVANT_POPULATION = 678865


def get_score_from_city_name_metric(metric: city_scorer.SuggestionMetric, city_name: str, partial_name: str):
    city_infos = provider_interface.CityInfos(
        city_name,
        [],
        IRRELEVANT_CITY_COORDINATES,
        IRRELEVANT_POPULATION
    )
    query = service.CitySuggestionsQuery(partial_name=partial_name)

    return metric.compute_score(city_infos, query)


def get_score_from_alt_city_name_metric(metric: city_scorer.SuggestionMetric, alt_city_names: List[str], partial_name: str):
    city_infos = provider_interface.CityInfos(
        "",
        alt_city_names,
        IRRELEVANT_CITY_COORDINATES,
        IRRELEVANT_POPULATION,
    )
    query = service.CitySuggestionsQuery(partial_name=partial_name)

    return metric.compute_score(city_infos, query)


def get_score_from_coordinates_metric(metric: city_scorer.SuggestionMetric,
                                      city_coordinates_tuple: Tuple, query_coordinate_tuple: Tuple):
    city_coordinates = provider_interface.CityCoordinates(*city_coordinates_tuple)
    city_infos = provider_interface.CityInfos(
        IRRELEVANT_CITY_NAME,
        [],
        city_coordinates,
        IRRELEVANT_POPULATION
    )
    query = service.CitySuggestionsQuery(
        partial_name=IRRELEVANT_CITY_NAME,
        latitude=query_coordinate_tuple[0],
        longitude=query_coordinate_tuple[1],
    )

    return metric.compute_score(city_infos, query)

def get_score_from_population_metric(metric: city_scorer.SuggestionMetric,
                                     city_population: int):
    city_infos = provider_interface.CityInfos(
        IRRELEVANT_CITY_NAME,
        [],
        IRRELEVANT_CITY_COORDINATES,
        city_population,
    )
    query = service.CitySuggestionsQuery(
        partial_name=IRRELEVANT_CITY_NAME,
    )

    return metric.compute_score(city_infos, query)
