# coding: utf-8
"""tests meteofrance module. Auth class"""
import pytest

from meteofrance import AuthMeteofrance, MeteofranceClient


@pytest.mark.parametrize("city", ["montreal", "Foix"])
def test_workflow(city):
    """Test classical workflow usage with the python library"""
    auth = AuthMeteofrance()
    client = MeteofranceClient(auth)

    list_places = client.search_places(city)
    my_place = list_places[0]

    my_place_weather_forecast = client.get_forecast(
        my_place.latitude, my_place.longitude
    )

    my_place_daily_forecast = my_place_weather_forecast.daily_forecast

    if my_place_weather_forecast.position["rain_product_available"] == 1:
        my_place_rain_forecast = client.get_rain(my_place.latitude, my_place.longitude)
        next_rain_dt = my_place_rain_forecast.next_rain_date_locale()

    my_place_wweather_alerts = client.get_warning_current_phenomenoms(my_place.admin2)
    # TODO: this methods of get_warning_full ?

    assert True
