# coding: utf-8
"""Tests Météo-France module. PictureOfTheDay class."""
from meteofrance_api import MeteoFranceClient


def test_picture_of_the_day() -> None:
    """Test weather picture of the day results from API."""
    client = MeteoFranceClient()

    potd = client.get_picture_of_the_day()

    assert "http://" in potd.image_url
    assert ".jpg" in potd.image_url
    assert "http://" in potd.image_hd_url
    assert ".jpg" in potd.image_hd_url
    assert potd.description
