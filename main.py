from src.web import flask_app_constructor
from src.suggestions.city_infos.geoname_gazetter_city_infos_provider import GeonameGazetterFileCityInfoProvider
from src.suggestions.service import CitySuggestionsService
from src.suggestions.domain import city_scorer

GEONAME_GAZETTER_FILE_PATH = "data/cities_canada-usa.tsv"

# noinspection Pylint
def main():

    # There should be a factory here somewhere
    city_infos_provider = GeonameGazetterFileCityInfoProvider(GEONAME_GAZETTER_FILE_PATH)
    city_scorer_implementation = city_scorer.CityScorer()
    city_suggestions = CitySuggestionsService(city_infos_provider, city_scorer_implementation)

    flask_app = flask_app_constructor.construct_app(city_suggestions)
    flask_app.run()


if __name__ == '__main__':
    main()
