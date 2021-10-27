"""Météo-France API test constants."""
from meteofrance_api.client import schema_place
from meteofrance_api.model import Place

MOUNTAIN_CITY: Place = schema_place.load(
    {
        "insee": "74080",
        "name": "La Clusaz",
        "lat": 45.90417,
        "lon": 6.42306,
        "country": "FR",
        "admin": "Rhône-Alpes",
        "admin2": "74",
        "postCode": "74220",
    }
)
