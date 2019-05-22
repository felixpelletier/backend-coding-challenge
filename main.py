import main_factory
from src.web import flask_app_constructor

city_suggestions = main_factory.create_application()
flask_app = flask_app_constructor.construct_app(city_suggestions)


# noinspection Pylint
def main():
    flask_app.run()


if __name__ == '__main__':
    main()
