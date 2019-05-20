
import difflib
import math

from src.suggestions.domain import city_scorer


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

        distance = self._compute_harvesine_distance(city_location, query_location)

        if distance > 0.0:
            return 1.0 / math.pow(distance, 1 / self.FALLOFF)
        else:
            return 1.0


    def _compute_harvesine_distance(self, city_location, query_location):
        """
            References:
                 - https://en.wikipedia.org/wiki/Haversine_formula
                 - https://en.wikipedia.org/wiki/Earth_radius#Mean_radius
        """
        EARTHS_RADIUS_KM = 6371.0

        city_latitude_rad, city_longitude_rad = self._coordinates_deg2rad(city_location)
        query_latitude_rad, query_longitude_rad = self._coordinates_deg2rad(query_location)

        delta_latitude = city_latitude_rad - query_latitude_rad
        delta_longitude = city_longitude_rad - query_longitude_rad

        # h = haversine of central angle
        h = self._haversine(delta_latitude) \
            + math.cos(query_latitude_rad) * math.cos(city_latitude_rad) * self._haversine(delta_longitude)

        distance = 2 * EARTHS_RADIUS_KM * math.asin(math.sqrt(h))

        return distance

    def _haversine(self, angle):
        return (1.0 - math.cos(angle)) / 2.0

    def _coordinates_deg2rad(self, location):
        latitude_deg, longitude_deg = location
        latitude_rad = math.radians(latitude_deg)
        longitude_rad = math.radians(longitude_deg)
        return latitude_rad, longitude_rad


