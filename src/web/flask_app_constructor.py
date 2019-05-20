from http import HTTPStatus
from flask import Flask, request, abort

from src.web.flask_utils import pretty_jsonify
from src.suggestions import service

QUERY_PARAMETER = 'q'
LONGITUDE_PARAMETER = 'longitude'
LATITUDE_PARAMETER = 'latitude'


def construct_app(city_suggestions):

    app = Flask(__name__)

    def convert_city_suggestion_to_dict(city_suggestion : service.CitySuggestion):
        return {
            "name": city_suggestion.name,
            "longitude": city_suggestion.longitude,
            "latitude": city_suggestion.latitude,
            "score": city_suggestion.score,
        }

    def convert_city_suggestions_response_to_dict(city_suggestion_response : service.CitySuggestionsResponse):
        return {
            "suggestions": [convert_city_suggestion_to_dict(city_suggestion)
                            for city_suggestion in city_suggestion_response.suggestions]
        }


    @app.route('/suggestions', methods=['GET'])
    def suggestions():

        input_query = request.args.get(QUERY_PARAMETER, "")

        try:
            longitude = convert_to_float_if_exists(request.args.get(LONGITUDE_PARAMETER, None))
            latitude = convert_to_float_if_exists(request.args.get(LATITUDE_PARAMETER, None))
        except ValueError:
            return abort(HTTPStatus.BAD_REQUEST)

        query = service.CitySuggestionsQuery(query=input_query, longitude=longitude, latitude=latitude)
        city_suggestions_response = city_suggestions.get_suggestions(query)
        response_dict = convert_city_suggestions_response_to_dict(city_suggestions_response)

        return pretty_jsonify(response_dict)

    return app


def convert_to_float_if_exists(parameter_string):
    if parameter_string is None:
        return None

    return float(parameter_string)




