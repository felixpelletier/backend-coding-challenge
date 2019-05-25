
from src.suggestions.city_infos.geoname_gazetter_city_infos_provider import GeonameGazetterFileCityInfoProvider
from src.suggestions.service import CitySuggestionsService
from src.suggestions.domain import city_scorer
from src.suggestions.domain import metrics
from src import yaml_metrics_factory

GEONAME_GAZETTER_FILE_PATH = "data/cities_canada-usa.tsv"
METRICS_CONFIGURATION_PATH = "metrics_config.yaml"


def create_application():
    city_infos_provider = GeonameGazetterFileCityInfoProvider(GEONAME_GAZETTER_FILE_PATH)

    city_scorer_implementation = city_scorer.CityScorer()
    yaml_metrics_factory.make_metrics(METRICS_CONFIGURATION_PATH)
    city_scorer_implementation.add_metric(metrics.NameStartsWithMetric(), 10)
    city_scorer_implementation.add_metric(metrics.LevenshteinCityNameSimilarityMetric(), 5)
    city_scorer_implementation.add_metric(metrics.HaversineLocationDistanceMetric(), 2)

    city_suggestions = CitySuggestionsService(city_infos_provider, city_scorer_implementation)

    return city_suggestions
