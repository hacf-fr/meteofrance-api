# coding: utf-8
"""Tests Météo-France module. Forecast class."""
from datetime import datetime

from meteofrance.client import MeteoFranceClient
from meteofrance.model import Place

from .const import MOUNTAIN_CITY


def test_forecast():
    """Test weather forecast results from API."""
    client = MeteoFranceClient()

    weather_forecast = client.get_forecast(latitude=48.8075, longitude=2.24028)
    now_ts = datetime.utcnow().timestamp()
    current_forecast = weather_forecast.current_forecast

    assert type(weather_forecast.position) == dict
    assert type(weather_forecast.updated_on) == int
    assert "T" in weather_forecast.daily_forecast[0].keys()
    assert "humidity" in weather_forecast.daily_forecast[0].keys()
    assert "rain" in weather_forecast.probability_forecast[0].keys()
    assert "clouds" in weather_forecast.forecast[0].keys()
    assert (
        type(
            weather_forecast.timestamp_to_locale_time(
                weather_forecast.daily_forecast[0]["dt"]
            )
        )
        == datetime
    )
    assert abs(weather_forecast.nearest_forecast["dt"] - now_ts) == min(
        [abs(x["dt"] - now_ts) for x in weather_forecast.forecast]
    )
    assert (
        current_forecast["dt"] < datetime.utcnow().timestamp()
        or not current_forecast["dt"]
    )
    assert (
        weather_forecast.today_forecast["dt"]
        == weather_forecast.daily_forecast[0]["dt"]
    )


def test_forecast_place():
    """Test weather forecast results from API."""
    client = MeteoFranceClient()

    weather_forecast = client.get_forecast_for_place(place=Place(MOUNTAIN_CITY))

    assert type(weather_forecast.position) == dict
    assert type(weather_forecast.updated_on) == int
    assert "T" in weather_forecast.daily_forecast[0].keys()
    assert "humidity" in weather_forecast.daily_forecast[0].keys()
    assert "rain" in weather_forecast.probability_forecast[0].keys()
    assert "clouds" in weather_forecast.forecast[0].keys()
    assert (
        type(
            weather_forecast.timestamp_to_locale_time(
                weather_forecast.daily_forecast[0]["dt"]
            )
        )
        == datetime
    )
