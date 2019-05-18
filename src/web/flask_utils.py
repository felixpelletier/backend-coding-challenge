
from http import HTTPStatus
import json

from flask import make_response


def pretty_jsonify(response_dict):
    """
        Pretty Json display for human consumption.
    """
    response = make_response(json.dumps(response_dict, indent=4))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = HTTPStatus.OK
    return response
