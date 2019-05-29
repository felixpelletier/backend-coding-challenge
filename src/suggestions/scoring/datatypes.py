
from dataclasses import dataclass


@dataclass
class CitySuggestionsQuery:
    partial_name: str
    latitude: float = None
    longitude: float = None


@dataclass
class CitySuggestion:
    name: str
    longitude: float
    latitude: float
    score: float
