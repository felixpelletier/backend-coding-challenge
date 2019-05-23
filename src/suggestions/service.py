
from dataclasses import dataclass, field
from typing import List
import itertools

from src.suggestions.city_infos import provider_interface
from src.suggestions.domain.datatypes import CitySuggestion, CitySuggestionsQuery


@dataclass
class CitySuggestionsResponse:
    suggestions: List[CitySuggestion] = field(default_factory=list)


class CitySuggestionsService:

    CITY_COUNT_TO_KEEP = 5

    def __init__(self, city_info_provider: provider_interface.CityInfoProvider, city_scorer):
        self.city_info_provider = city_info_provider
        self.city_scorer = city_scorer

    def get_suggestions(self, query: CitySuggestionsQuery) -> CitySuggestionsResponse:

        if not query.partial_name:
            return CitySuggestionsResponse(suggestions=[])

        cities_infos = self.city_info_provider.get_city_infos_list()
        cities_with_scores = [(city_infos, self.city_scorer.compute_score_for_city(city_infos, query))
                              for city_infos in cities_infos]
        selected_cities_with_score = self._select_best_suggestions(cities_with_scores)
        city_suggestions = [_build_city_suggestion_dto(city_infos, score)
                            for city_infos, score in selected_cities_with_score]

        return CitySuggestionsResponse(suggestions=city_suggestions)

    def _select_best_suggestions(self, cities_with_score):
        cities_sorted_by_score = reversed(sorted(cities_with_score, key=lambda city_with_score: city_with_score[1]))
        return itertools.islice(cities_sorted_by_score, self.CITY_COUNT_TO_KEEP)


def _build_city_suggestion_dto(city_infos, score):
    return CitySuggestion(
        name=city_infos['name'],
        longitude=city_infos['coordinates']['long'],
        latitude=city_infos['coordinates']['lat'],
        score=score,
    )
