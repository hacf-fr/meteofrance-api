# coding: utf-8
"""Tests for meteofrance modile. Forecast class."""
from datetime import datetime

from meteofrance.auth import AuthMeteofrance
from meteofrance.client import MeteofranceClient


def test_forecast():
    """Test weather forecast results from API."""
    auth = AuthMeteofrance()
    client = MeteofranceClient(auth)

    weather_forecast = client.get_forecast(latitude=48.8075, longitude=2.24028)

    assert [
        type(weather_forecast.position),
        type(weather_forecast.updated_on),
        "humidity" in weather_forecast.daily_forecast[0].keys(),
        "rain" in weather_forecast.probability_forecast[0].keys(),
        "clouds" in weather_forecast.forecast[0].keys(),
        type(
            weather_forecast.timestamp_to_locale_time(
                weather_forecast.daily_forecast[0]["dt"]
            )
        ),
    ] == [dict, int, True, True, True, datetime]
