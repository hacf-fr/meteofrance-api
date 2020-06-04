# coding: utf-8
"""Tests for meteofrance modile. Forecast class."""
from datetime import datetime

from meteofrance.auth import MeteoFranceAuth
from meteofrance.client import MeteoFranceClient
from meteofrance.model import Place

from .const import MOUNTAIN_CITY


def test_forecast():
    """Test weather forecast results from API."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

    weather_forecast = client.get_forecast(latitude=48.8075, longitude=2.24028)

    assert [
        type(weather_forecast.position),
        type(weather_forecast.updated_on),
        "T" in weather_forecast.daily_forecast[0].keys(),
        "humidity" in weather_forecast.daily_forecast[0].keys(),
        "rain" in weather_forecast.probability_forecast[0].keys(),
        "clouds" in weather_forecast.forecast[0].keys(),
        type(
            weather_forecast.timestamp_to_locale_time(
                weather_forecast.daily_forecast[0]["dt"]
            )
        ),
    ] == [dict, int, True, True, True, True, datetime]


def test_forecast_place():
    """Test weather forecast results from API."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

    weather_forecast = client.get_forecast_for_place(place=Place(MOUNTAIN_CITY))

    assert [
        type(weather_forecast.position),
        type(weather_forecast.updated_on),
        "T" in weather_forecast.daily_forecast[0].keys(),
        "humidity" in weather_forecast.daily_forecast[0].keys(),
        "rain" in weather_forecast.probability_forecast[0].keys(),
        "clouds" in weather_forecast.forecast[0].keys(),
        type(
            weather_forecast.timestamp_to_locale_time(
                weather_forecast.daily_forecast[0]["dt"]
            )
        ),
    ] == [dict, int, True, True, True, True, datetime]
