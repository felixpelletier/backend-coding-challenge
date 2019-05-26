
import dataclasses
from typing import List


@dataclasses.dataclass
class CityCoordinates:
    lat: float
    long: float


@dataclasses.dataclass
class CityInfos:
    name: str
    alt_names: List[str]
    coordinates: CityCoordinates
    population: int


class CityInfoProvider:

    def get_city_infos_list(self) -> List[CityInfos]:
        raise NotImplementedError


