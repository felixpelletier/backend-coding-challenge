import main_factory
from src.web import flask_app_constructor


# noinspection Pylint
def main():

    city_suggestions = main_factory.create_application()
    flask_app = flask_app_constructor.construct_app(city_suggestions)
    flask_app.run()


if __name__ == '__main__':
    main()
