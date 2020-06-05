# coding: utf-8
"""Tests Météo-France module. MeteoFranceSession class."""
import pytest
from requests.exceptions import RequestException

from meteofrance.session import MeteoFranceSession, MeteoFranceWSSession
from meteofrance.const import (
    METEOFRANCE_API_TOKEN,
    METEOFRANCE_API_URL,
    METEOFRANCE_WS_API_URL,
)


def test_session():
    """Test generic session."""
    session = MeteoFranceSession()

    resp = session.request("get", "places", params={"q": "montreal"})

    assert resp.status_code == 200


def test_session_wrong_token():
    """Test exceptions raised."""
    session = MeteoFranceSession("fake_token")

    with pytest.raises(RequestException):
        session.request("get", "places")
