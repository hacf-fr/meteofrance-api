# coding: utf-8
"""Tests Météo-France module. Place class."""
from meteofrance.client import MeteoFranceClient


def test_places() -> None:
    """Test for simple seach of Place."""
    client = MeteoFranceClient()

    list_places = client.search_places("montreal")

    assert list_places

    place = list_places[0]

    assert place.insee
    assert place.latitude
    assert place.longitude
    assert place.postal_code

    assert place.name == "Montréal"
    assert place.country == "FR"
    assert place.admin == "Languedoc-Roussillon"
    assert place.admin2 == "11"


def test_places_with_gps() -> None:
    """Test a place search by specifying a GPS point to search arround."""
    client = MeteoFranceClient()

    list_places = client.search_places("montreal", "45.50884", "-73.58")

    assert list_places

    place = list_places[0]

    assert place.name == "Montréal"
    assert place.country == "CA"
    assert place.admin == "Quebec"
    assert place.admin2 == "06"


def test_places_not_found() -> None:
    """Test when no places are found."""
    client = MeteoFranceClient()

    list_places = client.search_places("sqdmfkjdsmkf")

    assert not list_places


def test_places_print() -> None:
    """Test different way to print Places class."""
    client = MeteoFranceClient()

    place_in_france = client.search_places("montreal")[0]
    place_not_in_france = client.search_places("montreal", "45.50884", "-73.58")[0]

    assert (
        repr(place_in_france)
        == "<Place(name=Montréal, country=FR, admin=Languedoc-Roussillon)>"
    )
    assert str(place_in_france) == "Montréal - Languedoc-Roussillon (11) - FR"

    assert (
        repr(place_not_in_france) == "<Place(name=Montréal, country=CA, admin=Quebec)>"
    )
    assert str(place_not_in_france) == "Montréal - Quebec - CA"
    assert f"I live in {place_not_in_france}" == "I live in Montréal - Quebec - CA"
