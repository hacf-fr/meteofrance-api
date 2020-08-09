# coding: utf-8
"""Tests Météo-France module. MeteoFranceSession class."""
import pytest
from requests.exceptions import RequestException

from meteofrance.session import MeteoFranceSession


def test_session() -> None:
    """Test generic session."""
    session = MeteoFranceSession()

    resp = session.request("get", "places", params={"q": "montreal"})

    assert resp.status_code == 200


def test_session_wrong_token() -> None:
    """Test exceptions raised."""
    session = MeteoFranceSession("fake_token")

    with pytest.raises(RequestException):
        session.request("get", "places")
