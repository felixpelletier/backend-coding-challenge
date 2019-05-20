
import difflib
import math

from src.suggestions.domain import city_scorer
from src.suggestions.domain import haversine


class CityNameStartsWithSimilarityMetric(city_scorer.SuggestionMetric):

    def compute_score(self, city_infos, query):
        partial_name = query.query
        all_known_city_names = [city_infos['name']] + city_infos['alt_names']
        if any(self._starts_with(city_name, partial_name) for city_name in all_known_city_names):
            return 1.0
        else:
            return None

    def _starts_with(self, city_name, partial_name):
        return city_name.lower().startswith(partial_name.lower())


class RatcliffObershelpCityNameSimilarityMetric(city_scorer.SuggestionMetric):

    def compute_score(self, city_infos, query):
        partial_name = query.query
        all_known_city_names = [city_infos['name']] + city_infos['alt_names']
        return max(self._compute_name_distance(city_name, partial_name) for city_name in all_known_city_names)

    def _compute_name_distance(self, city_name, queried_name):
        """
        The standard library already implements the algorithm
        """
        return difflib.SequenceMatcher(a=city_name, b=queried_name).ratio()


class HaversineLocationDistanceMetric(city_scorer.SuggestionMetric):

    FALLOFF = 6.0

    def compute_score(self, city_infos, query):
        if query.longitude is None or query.latitude is None:
            return None

        city_location = (city_infos['coordinates']['lat'], city_infos['coordinates']['long'])
        query_location = (query.latitude, query.longitude)

        distance = haversine.compute_harvesine_distance(city_location, query_location)

        if distance > 0.0:
            return 1.0 / math.pow(distance, 1 / self.FALLOFF)
        else:
            return 1.0
