# coding: utf-8
"""Tests Météo-France module. Observation class."""
import time
from datetime import datetime, timezone, timedelta

from .const import MOUNTAIN_CITY
from meteofrance_api import MeteoFranceClient
from meteofrance_api.model import Place, Observation


def assert_types(observation: Observation) -> None:
    """Check observation types"""
    assert type(observation.timezone) == str
    assert type(observation.time_as_string) == str
    assert type(observation.time_as_datetime) == datetime
    assert type(observation.temperature) == float
    assert type(observation.wind_speed) == float
    assert type(observation.wind_direction) == int
    assert type(observation.wind_icon) == str
    assert type(observation.weather_icon) == str
    assert type(observation.weather_description) == str


def assert_datetime(observation: Observation) -> None:
    """Check observation time is before now but after now - 1h."""
    now = datetime.now(timezone.utc)
    assert True if observation.time_as_datetime is None else now - timedelta(hours=1) < observation.time_as_datetime < now


def test_observation_france() -> None:
    """Test weather observation results from API (valid result, from lat/lon)."""
    client = MeteoFranceClient()
    observation = client.get_observation(latitude=48.8075, longitude=2.24028)
    
    assert_types(observation)
    assert_datetime(observation)


def test_observation_world() -> None:
    """Test weather observation results from API (null result)."""
    client = MeteoFranceClient()
    observation = client.get_observation(latitude=45.5016889, longitude=73.567256)

    assert observation.timezone is None
    assert observation.time_as_string is None
    assert observation.time_as_datetime is None
    assert observation.temperature is None
    assert observation.wind_speed is None
    assert observation.wind_direction is None
    assert observation.wind_icon is None
    assert observation.weather_icon is None
    assert observation.weather_description is None


def test_observation_place() -> None:
    """Test weather observation results from API (valid result, from place)."""
    client = MeteoFranceClient()
    observation = client.get_observation_for_place(place=Place(MOUNTAIN_CITY))
    
    assert_types(observation)
    assert_datetime(observation)
