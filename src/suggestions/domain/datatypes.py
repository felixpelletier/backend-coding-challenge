
from dataclasses import dataclass, field

@dataclass
class CitySuggestionsQuery:
    query: str
    longitude: float = None
    latitude: float = None


@dataclass
class CitySuggestion:
    name: str
    longitude: float
    latitude: float
    score: float
