
import difflib
import Levenshtein
import math
import unicodedata

from src.suggestions.domain import city_scorer
from src.suggestions.domain import haversine


def normalize_name_for_comparison(name):
    return unicodedata.normalize("NFD", name).lower()


class ExactNameMatchMetric(city_scorer.SuggestionMetric):
    """
        This metric returns a score of 1.0 if the city's name is exactly with the query's partial name
        Otherwise, it returns None, therefore it is ignored
    """

    def compute_score(self, city_infos, query):
        all_known_city_names = [city_infos.name] + city_infos.alt_names
        if any(self._are_strings_equal(city_name, query.partial_name)
               for city_name in all_known_city_names):
            return 1.0
        else:
            return None

    @staticmethod
    def _are_strings_equal(str1: str, str2: str):
        return normalize_name_for_comparison(str1) == normalize_name_for_comparison(str2)


class NameStartsWithMetric(city_scorer.SuggestionMetric):
    """
        This metric returns a score of 1.0 if the city's name starts with the query's partial name
        Otherwise, it returns None, therefore it is ignored
    """

    def compute_score(self, city_infos, query):
        all_known_city_names = [city_infos.name] + city_infos.alt_names
        if any(self._starts_with(city_name, query.partial_name) for city_name in all_known_city_names):
            return 1.0
        else:
            return None

    @staticmethod
    def _starts_with(city_name, partial_name):
        normalized_city_name = normalize_name_for_comparison(city_name)
        normalized_partial_name = normalize_name_for_comparison(partial_name)
        return normalized_city_name.startswith(normalized_partial_name)


class RatcliffObershelpCityNameSimilarityMetric(city_scorer.SuggestionMetric):
    """
    WARNING: This class is untested.
             Running it on many city names results in poor performances.
             It's use is not recommended.

    """

    def compute_score(self, city_infos, query):
        all_known_city_names = [city_infos.name] + city_infos.alt_names
        return max(self._compute_name_similarity(city_name, query.partial_name) for city_name in all_known_city_names)

    @staticmethod
    def _compute_name_similarity(city_name, queried_name):
        # The standard library already implements the algorithm
        return difflib.SequenceMatcher(a=city_name, b=queried_name).ratio()


class LevenshteinCityNameSimilarityMetric(city_scorer.SuggestionMetric):
    """
        This metric implements the Levenshtein similarity metric.
        It first computes the Levenshtein distance between the city's name and the query's partial name
        Then, it computes the ratio between the Levenshtein distance and the sum of the lengths of the two strings.
        The result is a score between 0.0 (not similar) and 1.0 (exact match)
    """

    def compute_score(self, city_infos, query):
        all_known_city_names = [city_infos.name] + city_infos.alt_names
        return max(self._compute_name_similarity(city_name, query.partial_name) for city_name in all_known_city_names)

    @staticmethod
    def _compute_name_similarity(city_name, queried_name):
        return Levenshtein.ratio(
            normalize_name_for_comparison(city_name),
            normalize_name_for_comparison(queried_name),
        )


class HaversineLocationDistanceMetric(city_scorer.SuggestionMetric):
    """
        This metric uses the haversine distance between the city and the query.
        i.e: the approximate distance if the earth was a perfect sphere.

        The score is mapped on a bell curve, with a greater distance scoring lower.
        As an example:
        --------------------
        | distance | score |
        |    0     |  1.0  |
        |   300    |  0.83 |
        |  1000    |  0.14 |
        --------------------

    """

    STANDARD_DEVIATION = 500.0

    def compute_score(self, city_infos, query):
        if query.longitude is None or query.latitude is None:
            return None

        city_location = (city_infos.coordinates.lat, city_infos.coordinates.long)
        query_location = (query.latitude, query.longitude)

        distance = haversine.compute_harvesine_distance(city_location, query_location)
        print(distance)

        # Normal bell distribution with maximum at 1.0
        score = math.exp(-(1.0/2.0) * math.pow(distance/self.STANDARD_DEVIATION, 2))
        return max([0.0, score])


class LogarithmicPopulationMetric(city_scorer.SuggestionMetric):

    _HIGHEST_POPULATION = 8000000

    def compute_score(self, city_infos, query):
        population = min(city_infos.population, self._HIGHEST_POPULATION)
        if population <= 0:
            return 0.0

        return math.log10(population)/math.log10(self._HIGHEST_POPULATION)
