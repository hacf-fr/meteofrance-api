# coding: utf-8
"""Tests for meteofrance module. Place class."""

from meteofrance.auth import MeteoFranceAuth
from meteofrance.client import MeteoFranceClient


def test_places():
    """Test for simple seach of Place."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

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


def test_places_with_gps():
    """Test a place search by specifying a GPS point to search arround."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

    list_places = client.search_places("montreal", "45.50884", "-73.58")

    assert list_places

    place = list_places[0]

    assert place.name == "Montréal"
    assert place.country == "CA"
    assert place.admin == "Quebec"
    assert place.admin2 == "06"


def test_places_not_found():
    """Test when no places are found."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

    list_places = client.search_places("sqdmfkjdsmkf")

    assert not list_places


def test_places_print():
    """Test different way to print Places class."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

    place_in_france = client.search_places("montreal")[0]
    place_not_in_france = client.search_places("montreal", "45.50884", "-73.58")[0]

    assert (
        repr(place_in_france)
        == "<Place(name=Montréal, country=FR, admin=Languedoc-Roussillon)>"
    )
    assert str(place_in_france) == "Montréal - (11)"

    assert (
        repr(place_not_in_france) == "<Place(name=Montréal, country=CA, admin=Quebec)>"
    )
    assert str(place_not_in_france) == "Montréal - (Quebec)"
    assert f"I live in {place_not_in_france}" == "I live in Montréal - (Quebec)"
