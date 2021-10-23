# coding: utf-8
"""Tests Météo-France module. PictureOfTheDay class."""
from meteofrance_api import MeteoFranceClient


def test_picture_of_the_day() -> None:
    """Test weather picture of the day results from API."""
    client = MeteoFranceClient()

    potd = client.get_picture_of_the_day()

    assert potd.description
    assert potd.image_url == (
        "https://webservice.meteofrance.com/v2/report"
        "?domain=france&report_type=observation"
        "&report_subtype=image%20du%20jour&format=jpg"
        "&token=__Wj7dVSTjV9YGu1guveLyDq0g7S7TfTjaHBTPTpO0kj8__"
    )
