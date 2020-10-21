# coding: utf-8
"""Tests Météo-France module."""
import pytest

from meteofrance_api import MeteoFranceClient
from meteofrance_api.helpers import readeable_phenomenoms_dict


@pytest.mark.parametrize("city", ["montreal", "Foix"])
def test_workflow(city: str) -> None:
    """Test classical workflow usage with the Python library."""
    # Init client
    client = MeteoFranceClient()

    # Search a location from name.
    list_places = client.search_places(city)
    my_place = list_places[0]

    # Fetch weather forecast for the location
    my_place_weather_forecast = client.get_forecast_for_place(my_place)

    # Get the daily forecast
    my_place_daily_forecast = my_place_weather_forecast.daily_forecast

    # If rain in the hour forecast is available, get it.
    if my_place_weather_forecast.position["rain_product_available"] == 1:
        my_place_rain_forecast = client.get_rain(my_place.latitude, my_place.longitude)
        next_rain_dt = my_place_rain_forecast.next_rain_date_locale()
        if not next_rain_dt:
            rain_status = "No rain expected in the following hour."
        else:
            rain_status = next_rain_dt.strftime("%H:%M")
    else:
        rain_status = "No rain forecast available."

    # Fetch weather alerts.
    if my_place.admin2:
        my_place_weather_alerts = client.get_warning_current_phenomenoms(
            my_place.admin2
        )
        readable_warnings = readeable_phenomenoms_dict(
            my_place_weather_alerts.phenomenons_max_colors
        )

    assert type(my_place_daily_forecast) == list
    assert rain_status
    assert type(readable_warnings) == dict
