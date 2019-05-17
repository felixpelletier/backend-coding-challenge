
import flask_server
from GeonameGazetterCityInfoProvider import GeonameGazetterFileCityInfoProvider
from suggestions import CitySuggestions

city_infos_provider = GeonameGazetterFileCityInfoProvider("data/cities_canada-usa.tsv")
city_suggestions = CitySuggestions(city_infos_provider)

flask_app = flask_server.construct_app(city_suggestions)
flask_app.run()



