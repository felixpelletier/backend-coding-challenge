import copy
import random
import string

DEFAULT_COUNTRY = 'CA'
DEFAULT_LONGITUDE = 0.0
DEFAULT_LATITUDE = 0.0

FAKE_NAME_LENGTH = 10

SOME_RANDOM_SEED = 4456456


class FakeCityInfosProvider:

    def __init__(self):

        self.random_generator = random.Random(SOME_RANDOM_SEED)
        self.fake_city_infos = []

    def get_city_infos_list(self):
        return copy.deepcopy(self.fake_city_infos)

    def add_city_infos(self, city_infos):
        """
        Adds city infos to be used in the test

        :param city_infos: Some city infos, as given by any city info provider.
                           "name" is mendatory, while the rest of the fields are optionnal.
        """
        self.fake_city_infos.append({
            'name': city_infos['name'],
            'alt_names': city_infos.get('alt_names', []),
            'coordinates': {
                'lat': city_infos.get('coordinates', {}).get('lat', DEFAULT_LATITUDE),
                'long': city_infos.get('coordinates', {}).get('long', DEFAULT_LONGITUDE),
            },
            'country': city_infos.get('country', DEFAULT_COUNTRY),
        })

    def fill_with_random_data(self, city_count):
        for i in range(city_count):
            self.add_city_infos(generate_fake_city_infos(random_generator=self.random_generator))


def generate_fake_city_infos(fixed_data={}, random_generator=random.Random()):
    return {
        'name': fixed_data.get('name', _generate_fake_city_name(random_generator)),
        'alt_names': fixed_data.get('alt_names', []),
        'coordinates': {
            'lat': fixed_data.get('coordinates', {}).get('lat', DEFAULT_LATITUDE),
            'long': fixed_data.get('coordinates', {}).get('long', DEFAULT_LONGITUDE),
        },
        'country': fixed_data.get('country', DEFAULT_COUNTRY),
    }


def _generate_random_letter(random_generator):
    return random_generator.choice(string.ascii_lowercase)


def _generate_fake_city_name(random_generator=random.Random()):
    fake_name = ''.join(_generate_random_letter(random_generator) for i in range(FAKE_NAME_LENGTH))

