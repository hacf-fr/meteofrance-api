# coding: utf-8
"""Tests Météo-France module. Forecast class."""
import time
from datetime import datetime

from .const import MOUNTAIN_CITY
from meteofrance_api import MeteoFranceClient


def test_forecast_france() -> None:
    """Test weather forecast results from API."""
    client = MeteoFranceClient()

    weather_forecast = client.get_forecast(latitude=48.8075, longitude=2.24028)
    now_ts = int(time.time())

    assert type(weather_forecast.geometry) == dict
    assert type(weather_forecast.update_time) == int
    assert "T_max" in weather_forecast.properties["daily_forecast"][0].keys()
    assert (
        "relative_humidity_max"
        in weather_forecast.properties["daily_forecast"][0].keys()
    )
    assert "rain_hazard_3h" in weather_forecast.probability_forecast[0].keys()
    assert "total_cloud_cover" in weather_forecast.properties["forecast"][0].keys()
    assert (
        type(
            weather_forecast.timestamp_to_locale_time(
                weather_forecast.properties["daily_forecast"][0]["time"]
            )
        )
        == datetime
    )
    assert abs(weather_forecast.nearest_forecast["time"] - now_ts) <= 30 * 60
    assert now_ts - 3600 <= weather_forecast.current_forecast["time"] <= now_ts
    assert (
        weather_forecast.today_forecast["time"]
        == weather_forecast.properties["daily_forecast"][0]["time"]
    )


def test_forecast_world() -> None:
    """Test weather forecast results from API."""
    client = MeteoFranceClient()

    weather_forecast = client.get_forecast(latitude=45.5016889, longitude=73.567256)
    now_ts = int(time.time())

    assert type(weather_forecast.geometry) == dict
    assert type(weather_forecast.update_time) == int
    assert "T_max" in weather_forecast.properties["daily_forecast"][0].keys()
    assert (
        "relative_humidity_max"
        in weather_forecast.properties["daily_forecast"][0].keys()
    )
    assert not weather_forecast.probability_forecast
    assert "total_cloud_cover" in weather_forecast.properties["forecast"][0].keys()
    assert (
        type(
            weather_forecast.timestamp_to_locale_time(
                weather_forecast.properties["daily_forecast"][0]["time"]
            )
        )
        == datetime
    )
    assert abs(weather_forecast.nearest_forecast["time"] - now_ts) == min(
        abs(x["time"] - now_ts) for x in weather_forecast.properties["forecast"]
    )
    assert (
        weather_forecast.current_forecast["time"]
        == weather_forecast.nearest_forecast["time"]
    )
    assert (
        weather_forecast.today_forecast["time"]
        == weather_forecast.properties["daily_forecast"][0]["time"]
    )


def test_forecast_place() -> None:
    """Test weather forecast results from API."""
    client = MeteoFranceClient()

    weather_forecast = client.get_forecast_for_place(place=MOUNTAIN_CITY)

    assert type(weather_forecast.geometry) == dict
    assert type(weather_forecast.update_time) == int
    assert "T_max" in weather_forecast.properties["daily_forecast"][0].keys()
    assert (
        "relative_humidity_max"
        in weather_forecast.properties["daily_forecast"][0].keys()
    )
    assert "rain_hazard_3h" in weather_forecast.probability_forecast[0].keys()
    assert "total_cloud_cover" in weather_forecast.properties["forecast"][0].keys()
    assert (
        type(
            weather_forecast.timestamp_to_locale_time(
                weather_forecast.properties["daily_forecast"][0]["time"]
            )
        )
        == datetime
    )
