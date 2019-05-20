
import http
import urllib.parse

import pytest

from src.web import flask_app_constructor
from src.suggestions import service
from tests.suggestions import service_fakes

ROOT_PATH = "/"
SUGGESTIONS_PATH = "/suggestions"

SOME_CITY_SUGGESTION = service.CitySuggestion(name="SOME_NAME", latitude=3, longitude=5, score=42)


def get(client, path, data):
    url = path + "?" + urllib.parse.urlencode(data)
    return client.get(url)

@pytest.fixture
def fake_service():
    return service_fakes.FakeSuggestionService()


@pytest.fixture
def client(fake_service):
    app = flask_app_constructor.construct_app(fake_service)
    client = app.test_client()
    yield client


def test_getting_root_returns_HTTP_NOT_FOUND(client):
    response = client.get(ROOT_PATH)
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_given_empty_query_when_getting_suggestions_returns_HTTP_OK(client):
    response = client.get(SUGGESTIONS_PATH)
    assert response.status_code == http.HTTPStatus.OK


def test_given_invalid_latitude_when_getting_suggestions_returns_HTTP_BAD_REQUEST(client):
    response = get(client, SUGGESTIONS_PATH, {"latitude": "An invalid latitude"})
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_given_invalid_longitude_when_getting_suggestions_returns_HTTP_BAD_REQUEST(client):
    response = get(client, SUGGESTIONS_PATH, {"longitude": "An invalid longitude"})
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_given_no_suggestions_when_getting_suggestions_returns_empty_suggestion_list(client):
    response = get(client, SUGGESTIONS_PATH, {})
    json_data = response.get_json()
    assert len(json_data["suggestions"]) == 0


def test_given_some_suggestions_when_getting_suggestions_returns_corresponding_amount_of_suggestions(client, fake_service):
    some_expected_suggestions_count = 54
    service_suggestions = [SOME_CITY_SUGGESTION] * some_expected_suggestions_count
    service_response = service.CitySuggestionsResponse(service_suggestions)
    fake_service.set_response(service_response)

    response = get(client, SUGGESTIONS_PATH, {})
    json_data = response.get_json()

    assert len(json_data["suggestions"]) == some_expected_suggestions_count


def test_given_some_suggestion_when_getting_suggestions_returns_proper_suggestion_name(client, fake_service):
    service_response = service.CitySuggestionsResponse([SOME_CITY_SUGGESTION])
    fake_service.set_response(service_response)

    response = get(client, SUGGESTIONS_PATH, {})
    json_data = response.get_json()
    actual_suggestion = json_data["suggestions"][0]

    assert actual_suggestion["name"] == SOME_CITY_SUGGESTION.name


def test_given_some_suggestion_when_getting_suggestions_returns_proper_score(client, fake_service):
    service_response = service.CitySuggestionsResponse([SOME_CITY_SUGGESTION])
    fake_service.set_response(service_response)

    response = get(client, SUGGESTIONS_PATH, {})
    json_data = response.get_json()
    actual_suggestion = json_data["suggestions"][0]

    assert actual_suggestion["score"] == SOME_CITY_SUGGESTION.score


def test_given_some_suggestion_when_getting_suggestions_returns_proper_city_position(client, fake_service):
    service_response = service.CitySuggestionsResponse([SOME_CITY_SUGGESTION])
    fake_service.set_response(service_response)

    response = get(client, SUGGESTIONS_PATH, {})
    json_data = response.get_json()
    actual_suggestion = json_data["suggestions"][0]

    assert actual_suggestion["latitude"] == SOME_CITY_SUGGESTION.latitude
    assert actual_suggestion["longitude"] == SOME_CITY_SUGGESTION.longitude
