
import pytest
import tempfile
import collections
import typing
import contextlib
import os

from src.suggestions.city_infos import geoname_gazetter_city_infos_provider as provider

defaults = [
    ("id", "3"),
    ("name", "Québec"),
    ("ascii", "Quebec"),
    ("alt_name", ""),
    ("lat", "49.0534"),
    ("long", "-33.444"),
    ("feat_class", "P"),
    ("feat_code", "PPL"),
    ("country", "CA"),
    ("cc2", "03"),
    ("admin1", "34874"),
    ("admin2", ""),
    ("admin3", ""),
    ("admin4", "3242"),
    ("population", "50000"),
    ("elevation", ""),
    ("dem", ""),
    ("tz", "America/Vancouver"),
    ("modified_at", "2013-02-12"),
]


def get_default_line_attributes() -> collections.OrderedDict:
    return collections.OrderedDict(defaults)


def attribute_dict_to_string(attributes: collections.OrderedDict):
    return "\t".join(attributes.values())


def city_infos_to_string(cities_infos: typing.List[collections.OrderedDict]):
    return "\n".join(attribute_dict_to_string(single_city_infos) for single_city_infos in cities_infos)

@contextlib.contextmanager
def generate_test_file(cities_infos: typing.List[collections.OrderedDict]):
    file_path = None
    with tempfile.NamedTemporaryFile("w", delete=False) as temp_file:
        header = "\t".join(key for key, value in defaults)
        temp_file.write(header + "\n")
        temp_file.write(city_infos_to_string(cities_infos))
        file_path = temp_file.name

    yield provider.GeonameGazetterFileCityInfoProvider(file_path)
    os.remove(file_path)


def test_one_line_file():
    with generate_test_file([get_default_line_attributes()]) as geoname_provider:
        assert len(geoname_provider.get_city_infos_list()) == 1


def test_multiline_file():
    expected_line_count = 5
    test_data = [get_default_line_attributes()] * expected_line_count
    with generate_test_file(test_data) as geoname_provider:
        assert len(geoname_provider.get_city_infos_list()) == expected_line_count


def test_name():
    expected_name = "Paris"
    city_infos = get_default_line_attributes()
    city_infos["name"] = expected_name
    with generate_test_file([city_infos]) as geoname_provider:
        assert geoname_provider.get_city_infos_list()[0].name == expected_name


def test_alternative_names():
    expected_alt_names = ["Paris", "Parisse", "Paresse"]
    city_infos = get_default_line_attributes()
    city_infos["alt_name"] = "Paris,Parisse,Paresse"
    with generate_test_file([city_infos]) as geoname_provider:
        assert geoname_provider.get_city_infos_list()[0].alt_names == expected_alt_names


def test_empty_alternative_names():
    expected_alt_names = []
    city_infos = get_default_line_attributes()
    city_infos["alt_name"] = ""
    with generate_test_file([city_infos]) as geoname_provider:
        assert geoname_provider.get_city_infos_list()[0].alt_names == expected_alt_names


def test_coordinates():
    expected_lat = 24.654
    expected_long = -18.444
    city_infos = get_default_line_attributes()
    city_infos["lat"] = str(expected_lat)
    city_infos["long"] = str(expected_long)
    with generate_test_file([city_infos]) as geoname_provider:
        coordinates = geoname_provider.get_city_infos_list()[0].coordinates
        assert coordinates.lat == expected_lat
        assert coordinates.long == expected_long

def test_population():
    expected_population = 678963
    city_infos = get_default_line_attributes()
    city_infos["population"] = str(expected_population)
    with generate_test_file([city_infos]) as geoname_provider:
        assert geoname_provider.get_city_infos_list()[0].population == expected_population
