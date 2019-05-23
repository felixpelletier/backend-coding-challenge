
import dataclasses
from typing import List

class CityInfoProvider:

    def get_city_infos_list(self):
        raise NotImplementedError


@dataclasses.dataclass
class CityCoordinates:
    lat: float
    long: float


@dataclasses.dataclass
class CityInfos:
    name: str
    alt_names: List[str]
    coordinates: CityCoordinates
    country: str



