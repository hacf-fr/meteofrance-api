# coding: utf-8
"""tests for meteofrance modile. Forecast class"""
import pytest

import requests
from datetime import datetime

from meteofrance import AuthMeteofrance, MeteofranceClient
from meteofrance.const import METEOFRANCE_API_URL, METEOFRANCE_API_TOKEN


def test_rain():
    """Test rain forecast on a covered zone"""
    auth = AuthMeteofrance()
    client = MeteofranceClient(auth)

    rain = client.get_rain(latitude=48.8075, longitude=2.24028)

    assert [
        type(rain.position),
        type(rain.updated_on),
        type(rain.quality),
        "rain" in rain.forecast[0].keys(),
    ] == [dict, int, int, True]


def test_rain_not_covered():
    """Test rain forecast result on a non covered zone"""
    auth = AuthMeteofrance()
    client = MeteofranceClient(auth)

    with pytest.raises(requests.HTTPError, match=r"400 .*"):
        rain = client.get_rain(latitude=45.508, longitude=-73.58)


def test_rain_expected(requests_mock):
    """Test datecomputation when rain is expected within the hour."""
    auth = AuthMeteofrance()
    client = MeteofranceClient(auth)

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
    assert f"{date_rain}" == "2020-05-20 19:50:00+02:00"
