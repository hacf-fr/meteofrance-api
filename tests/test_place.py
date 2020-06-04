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

    assert [
        place.insee is not None,
        place.name is not None,
        place.latitude is not None,
        place.longitude is not None,
        place.postal_code is not None,
    ] == [True, True, True, True, True]

    assert [place.country, place.admin] == ["FR", "Languedoc-Roussillon"]


def test_places_with_gps():
    """Test a place search by specifying a GPS point to search arround."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

    list_places = client.search_places("montreal", "45.50884", "-73.58")

    assert list_places

    place = list_places[0]

    assert [place.country, place.admin] == ["CA", "Quebec"]


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
