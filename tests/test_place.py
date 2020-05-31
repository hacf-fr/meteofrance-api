# coding: utf-8
"""tests for meteofrance module. Place class"""

from meteofrance.auth import AuthMeteofrance
from meteofrance.client import MeteofranceClient


def test_places():
    """Test for simple seach of Place"""
    auth = AuthMeteofrance()
    client = MeteofranceClient(auth)

    list_places = client.search_places("montreal")
    place = list_places[0]

    assert [
        place.insee is not None,
        place.name is not None,
        place.latitude is not None,
        place.longitude is not None,
        place.country is not None,
        place.admin is not None,
        place.postcode is not None,
    ] == [True, True, True, True, True, True, True]


def test_places_with_gps():
    """Test a place search by specifying a GPS point to search arround"""
    auth = AuthMeteofrance()
    client = MeteofranceClient(auth)

    list_places = client.search_places("montreal", "45.50884", "-73.58")
    place = list_places[0]

    assert [place.country, place.admin] == ["CA", "Quebec"]


def test_places_not_found():
    """Test when no places are found"""
    auth = AuthMeteofrance()
    client = MeteofranceClient(auth)

    list_places = client.search_places("sqdmfkjdsmkf")

    assert not list_places


def test_places_print():
    """Test different way to print Places class"""
    auth = AuthMeteofrance()
    client = MeteofranceClient(auth)

    place_not_in_france = client.search_places("montreal", "45.50884", "-73.58")[0]
    place_in_france = client.search_places("montreal")[0]

    assert [
        "{}".format(place_in_france),
        place_in_france.pretty_print(),
        place_not_in_france.pretty_print(),
    ] == [
        "<Place(name=Montréal, country=FR, admin=Languedoc-Roussillon)>",
        "Montréal - (11)",
        "Montréal - (Quebec)",
    ]
