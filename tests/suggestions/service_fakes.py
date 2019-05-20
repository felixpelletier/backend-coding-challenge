
from src.suggestions import service


class FakeSuggestionService:

    def __init__(self):
        self._response = service.CitySuggestionsResponse()
        self._latest_query = None

    def set_response(self, response: service.CitySuggestionsResponse):
        self._response = response

    @property
    def latest_query(self) -> service.CitySuggestionsQuery:
        return self._latest_query

    def get_suggestions(self, query: service.CitySuggestionsQuery) -> service.CitySuggestionsResponse:
        self._latest_query = query
        return self._response
