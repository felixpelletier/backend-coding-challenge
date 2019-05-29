
import os.path

from src.suggestions.city_infos.geoname_gazetter_city_infos_provider import GeonameGazetterFileCityInfoProvider
from src.suggestions.service import CitySuggestionsService
from src.suggestions.scoring import city_scorer
from src import yaml_metrics_factory

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GEONAME_GAZETTER_FILE_PATH = os.path.join(ROOT_DIR, "data/cities_canada-usa.tsv")
METRICS_CONFIGURATION_PATH = os.path.join(ROOT_DIR, "metrics_config.yaml")


def _create_city_scorer():
    city_scorer_implementation = city_scorer.CityScorer()
    metrics_factory = yaml_metrics_factory.YamlMetricsFactory.from_file_path(METRICS_CONFIGURATION_PATH)
    for metric, weight in metrics_factory.make_metrics():
        city_scorer_implementation.add_metric(metric, weight)
    return city_scorer_implementation


def create_application():
    city_infos_provider = GeonameGazetterFileCityInfoProvider(GEONAME_GAZETTER_FILE_PATH)
    city_scorer_implementation = _create_city_scorer()
    city_suggestions = CitySuggestionsService(city_infos_provider, city_scorer_implementation)

    return city_suggestions
