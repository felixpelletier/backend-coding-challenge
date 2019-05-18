from http import HTTPStatus
from flask import Flask, request, abort

from src.web.flask_utils import pretty_jsonify
from src.suggestions.service import CitySuggestionsQuery

QUERY_PARAMETER = 'q'
LONGITUDE_PARAMETER = 'longitude'
LATITUDE_PARAMETER = 'latitude'


def construct_app(city_suggestions):

    app = Flask(__name__)

    @app.route('/suggestions', methods=['GET'])
    def suggestions():

        input_query = request.args.get(QUERY_PARAMETER, "")

        try:
            longitude = convert_to_float_if_exists(request.args.get(LONGITUDE_PARAMETER, None))
            latitude = convert_to_float_if_exists(request.args.get(LATITUDE_PARAMETER, None))
        except ValueError:
            return abort(HTTPStatus.BAD_REQUEST)

        query = CitySuggestionsQuery(query=input_query, longitude=longitude, latitude=latitude)
        response = city_suggestions.get_suggestions(query)

        return pretty_jsonify(response)

    return app


def convert_to_float_if_exists(parameter_string):
    if parameter_string is None:
        return None

    return float(parameter_string)




