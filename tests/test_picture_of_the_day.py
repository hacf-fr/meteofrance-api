# coding: utf-8
"""Tests Météo-France module. PictureOfTheDay class."""
from unittest.mock import Mock

from tests.fixtures import get_file_content

from meteofrance_api import MeteoFranceClient
from meteofrance_api.const import METEOFRANCE_API_URL


def test_picture_of_the_day(requests_mock: Mock) -> None:
    """Test weather picture of the day results from API."""
    client = MeteoFranceClient()

    requests_mock.request(
        "get",
        f"{METEOFRANCE_API_URL}/report",
        text=get_file_content("tests/fixtures/report_picture_du_jour.txt"),
    )

    potd = client.get_picture_of_the_day()

    assert potd.description
    assert potd.image_url == (
        "https://webservice.meteofrance.com/v2/report"
        "?domain=france&report_type=observation"
        "&report_subtype=image%20du%20jour&format=jpg"
        "&token=__Wj7dVSTjV9YGu1guveLyDq0g7S7TfTjaHBTPTpO0kj8__"
    )
