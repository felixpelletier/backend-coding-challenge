
import main_factory
from src.suggestions import service


def test_construct_app():
    main_factory.create_application()


def test_simple_query():
    app = main_factory.create_application()
    query = service.CitySuggestionsQuery(
        partial_name="Québec",
        latitude=-71.21454,
        longitude=46.81228,
    )
    suggestions_dto = app.get_suggestions(query)
    assert any(suggestion.name == "Québec" for suggestion in suggestions_dto.suggestions)
