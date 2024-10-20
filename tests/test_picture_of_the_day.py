"""Tests Météo-France module. PictureOfTheDay class."""
from meteofrance_api import const
from meteofrance_api import MeteoFranceClient


def test_picture_of_the_day() -> None:
    """Test weather picture of the day results from API."""
    client = MeteoFranceClient()

    potd = client.get_picture_of_the_day()

    assert potd.description
    params = "?domain=france&report_type=observation&report_subtype=image%20du%20jour&format=jpg"
    token_param = f"&token={const.METEOFRANCE_API_TOKEN}"
    path = "/v2/report"
    assert_url = f"{const.METEOFRANCE_API_URL}{path}{params}{token_param}"
    assert potd.image_url == assert_url
