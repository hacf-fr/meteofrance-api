# coding: utf-8
"""Tests Météo-France module. Observation class."""
import time
from datetime import datetime, timezone, timedelta

from .const import MOUNTAIN_CITY
from meteofrance_api import MeteoFranceClient
from meteofrance_api.model import Place


def test_observation_france() -> None:
    """Test weather observation results from API."""
    client = MeteoFranceClient()

    weather_observation = client.get_observation(latitude=48.8075, longitude=2.24028)
    now = datetime.now(timezone.utc)

    assert type(weather_observation.timezone) == str
    assert type(weather_observation.time_as_string) == str
    assert type(weather_observation.time_as_datetime) == datetime
    assert type(weather_observation.temperature) == float
    assert type(weather_observation.wind_speed) == float
    assert type(weather_observation.wind_direction) == int
    assert type(weather_observation.wind_icon) == str
    assert type(weather_observation.weather_icon) == str
    assert type(weather_observation.weather_description) == str

    assert now - timedelta(hours=1) < weather_observation.time_as_datetime < now


def test_observation_world() -> None:
    """Test weather observation results from API."""
    client = MeteoFranceClient()

    weather_observation = client.get_observation(latitude=45.5016889, longitude=73.567256)

    assert weather_observation.timezone is None
    assert weather_observation.time_as_string is None
    assert weather_observation.time_as_datetime is None
    assert weather_observation.temperature is None
    assert weather_observation.wind_speed is None
    assert weather_observation.wind_direction is None
    assert weather_observation.wind_icon is None
    assert weather_observation.weather_icon is None
    assert weather_observation.weather_description is None


def test_observation_place() -> None:
    """Test weather observation results from API."""
    client = MeteoFranceClient()

    weather_observation = client.get_observation_for_place(place=Place(MOUNTAIN_CITY))
    now = datetime.now(timezone.utc)

    assert type(weather_observation.timezone) == str
    assert type(weather_observation.time_as_string) == str
    assert type(weather_observation.time_as_datetime) == datetime
    assert type(weather_observation.temperature) == float
    assert type(weather_observation.wind_speed) == float
    assert type(weather_observation.wind_direction) == int
    assert type(weather_observation.wind_icon) == str
    assert type(weather_observation.weather_icon) == str
    assert type(weather_observation.weather_description) == str

    assert now - timedelta(hours=1) < weather_observation.time_as_datetime < now
