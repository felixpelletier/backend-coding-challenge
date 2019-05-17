
from dataclasses import dataclass

@dataclass
class CitySuggestionsQuery:
    query: str
    longitude: float = None
    latitude: float = None

@dataclass
class CitySuggestionsResponse:
    query: str
    longitude: float = None
    latitude: float = None


# TODO: Find a better name.
class CitySuggestions:

    def __init__(self, city_info_provider):
        self.city_info_provider = city_info_provider

    def get_suggestions(self, query: CitySuggestionsQuery):
        return self.city_info_provider.get_city_infos_list()
        return {
            "suggestions": [
                {
                    "name": "London, ON, Canada",
                    "latitude": "42.98339",
                    "longitude": "-81.23304",
                    "score": 0.9,
                },
                {
                    "name": "London, OH, USA",
                    "latitude": "39.88645",
                    "longitude": "-83.44825",
                    "score": 0.5,
                },
                {
                    "name": "London, KY, USA",
                    "latitude": "37.12898",
                    "longitude": "-84.08326",
                    "score": 0.5,
                },
                {
                    "name": "Londontowne, MD, USA",
                    "latitude": "38.93345",
                    "longitude": "-76.54941",
                    "score": 0.3,
                },
            ]
        }
