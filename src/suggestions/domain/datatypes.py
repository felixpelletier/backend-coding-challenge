
from dataclasses import dataclass, field

@dataclass
class CitySuggestionsQuery:
    partial_name: str
    longitude: float = None
    latitude: float = None


@dataclass
class CitySuggestion:
    name: str
    longitude: float
    latitude: float
    score: float
