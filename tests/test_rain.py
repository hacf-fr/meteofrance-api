# coding: utf-8
"""Tests Météo-France module. Forecast class."""
from unittest.mock import Mock

import pytest
import requests

from meteofrance_api import MeteoFranceClient
from meteofrance_api.const import METEOFRANCE_API_URL


def test_rain() -> None:
    """Test rain forecast on a covered zone."""
    client = MeteoFranceClient()

    rain = client.get_rain(latitude=48.8075, longitude=2.24028)

    assert type(rain.position) == dict
    assert type(rain.updated_on) == int
    assert type(rain.quality) == int
    assert "rain" in rain.forecast[0].keys()


def test_rain_not_covered() -> None:
    """Test rain forecast result on a non covered zone."""
    client = MeteoFranceClient()

    with pytest.raises(requests.HTTPError, match=r"400 .*"):
        client.get_rain(latitude=45.508, longitude=-73.58)


def test_rain_expected(requests_mock: Mock) -> None:
    """Test datecomputation when rain is expected within the hour."""
    client = MeteoFranceClient()

    requests_mock.request(
        "get",
        f"{METEOFRANCE_API_URL}/rain",
        json={
            "position": {
                "lat": 48.807166,
                "lon": 2.239895,
                "alti": 76,
                "name": "Meudon",
                "country": "FR - France",
                "dept": "92",
                "timezone": "Europe/Paris",
            },
            "updated_on": 1589995200,
            "quality": 0,
            "forecast": [
                {"dt": 1589996100, "rain": 1, "desc": "Temps sec"},
                {"dt": 1589996400, "rain": 1, "desc": "Temps sec"},
                {"dt": 1589996700, "rain": 1, "desc": "Temps sec"},
                {"dt": 1589997000, "rain": 2, "desc": "Pluie faible"},
                {"dt": 1589997300, "rain": 3, "desc": "Pluie modérée"},
                {"dt": 1589997600, "rain": 2, "desc": "Pluie faible"},
                {"dt": 1589998200, "rain": 1, "desc": "Temps sec"},
                {"dt": 1589998800, "rain": 1, "desc": "Temps sec"},
                {"dt": 1589999400, "rain": 1, "desc": "Temps sec"},
            ],
        },
    )

    rain = client.get_rain(latitude=48.8075, longitude=2.24028)
    date_rain = rain.next_rain_date_locale()
    assert str(date_rain) == "2020-05-20 19:50:00+02:00"
    assert (
        str(rain.timestamp_to_locale_time(rain.forecast[3]["dt"]))
        == "2020-05-20 19:50:00+02:00"
    )


def test_no_rain_expected(requests_mock: Mock) -> None:
    """Test datecomputation when rain is expected within the hour."""
    client = MeteoFranceClient()

    requests_mock.request(
        "get",
        f"{METEOFRANCE_API_URL}/rain",
        json={
            "position": {
                "lat": 48.807166,
                "lon": 2.239895,
                "alti": 76,
                "name": "Meudon",
                "country": "FR - France",
                "dept": "92",
                "timezone": "Europe/Paris",
            },
            "updated_on": 1589995200,
            "quality": 0,
            "forecast": [
                {"dt": 1589996100, "rain": 1, "desc": "Temps sec"},
                {"dt": 1589996400, "rain": 1, "desc": "Temps sec"},
                {"dt": 1589996700, "rain": 1, "desc": "Temps sec"},
                {"dt": 1589997000, "rain": 1, "desc": "Temps sec"},
                {"dt": 1589997300, "rain": 1, "desc": "Temps sec"},
                {"dt": 1589997600, "rain": 1, "desc": "Temps sec"},
                {"dt": 1589998200, "rain": 1, "desc": "Temps sec"},
                {"dt": 1589998800, "rain": 1, "desc": "Temps sec"},
                {"dt": 1589999400, "rain": 1, "desc": "Temps sec"},
            ],
        },
    )

    rain = client.get_rain(latitude=48.8075, longitude=2.24028)
    assert rain.next_rain_date_locale() is None
