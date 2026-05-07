"""Tests Météo-France module. Forecast class."""

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from .const import MOUNTAIN_CITY
from meteofrance_api import MeteoFranceClient
from meteofrance_api.model import Place
from meteofrance_api.model.forecast import DailyForecast
from meteofrance_api.model.forecast import ForecastPosition
from meteofrance_api.model.forecast import HourlyForecast
from meteofrance_api.model.forecast import ProbabilityForecast


def test_forecast_france() -> None:
    """Test weather forecast results from API."""
    client = MeteoFranceClient()

    weather_forecast = client.get_forecast(latitude=48.8075, longitude=2.24028)
    now = datetime.now(timezone.utc)

    assert isinstance(weather_forecast.position, ForecastPosition)
    assert isinstance(weather_forecast.updated_on, int)
    assert isinstance(weather_forecast.daily_forecast[0], DailyForecast)
    assert isinstance(weather_forecast.forecast[0], HourlyForecast)
    assert isinstance(weather_forecast.probability_forecast[0], ProbabilityForecast)
    assert isinstance(
        weather_forecast.iso_to_locale_time(weather_forecast.daily_forecast[0].time),
        datetime,
    )

    nearest = weather_forecast.nearest_forecast
    nearest_time = datetime.fromisoformat(nearest.time.replace("Z", "+00:00"))
    assert abs((nearest_time - now).total_seconds()) <= 30 * 60

    current = weather_forecast.current_forecast
    current_time = datetime.fromisoformat(current.time.replace("Z", "+00:00"))
    assert now - timedelta(hours=1) <= current_time <= now

    assert weather_forecast.today_forecast.time == weather_forecast.daily_forecast[0].time


def test_forecast_world() -> None:
    """Test weather forecast results from API."""
    client = MeteoFranceClient()

    weather_forecast = client.get_forecast(latitude=45.5016889, longitude=73.567256)
    now = datetime.now(timezone.utc)

    assert isinstance(weather_forecast.position, ForecastPosition)
    assert isinstance(weather_forecast.updated_on, int)
    assert isinstance(weather_forecast.daily_forecast[0], DailyForecast)
    assert isinstance(weather_forecast.forecast[0], HourlyForecast)
    assert not weather_forecast.probability_forecast
    assert isinstance(
        weather_forecast.iso_to_locale_time(weather_forecast.daily_forecast[0].time),
        datetime,
    )

    nearest = weather_forecast.nearest_forecast
    nearest_time = datetime.fromisoformat(nearest.time.replace("Z", "+00:00"))
    min_distance = min(
        abs((datetime.fromisoformat(x.time.replace("Z", "+00:00")) - now).total_seconds())
        for x in weather_forecast.forecast
    )
    assert abs((nearest_time - now).total_seconds()) == min_distance

    assert weather_forecast.current_forecast.time == weather_forecast.nearest_forecast.time
    assert weather_forecast.today_forecast.time == weather_forecast.daily_forecast[0].time


def test_forecast_place() -> None:
    """Test weather forecast results from API."""
    client = MeteoFranceClient()

    weather_forecast = client.get_forecast_for_place(place=Place(MOUNTAIN_CITY))

    assert isinstance(weather_forecast.position, ForecastPosition)
    assert isinstance(weather_forecast.updated_on, int)
    assert isinstance(weather_forecast.daily_forecast[0], DailyForecast)
    assert isinstance(weather_forecast.forecast[0], HourlyForecast)
    assert isinstance(weather_forecast.probability_forecast[0], ProbabilityForecast)
    assert isinstance(
        weather_forecast.iso_to_locale_time(weather_forecast.daily_forecast[0].time),
        datetime,
    )
