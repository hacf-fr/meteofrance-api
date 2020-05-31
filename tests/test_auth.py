# coding: utf-8
"""tests meteofrance module. Auth class"""
import pytest
import requests

from meteofrance.auth import Auth, AuthMeteofrance
from meteofrance.const import METEOFRANCE_API_TOKEN, METEOFRANCE_API_URL


def test_auth():

    auth = Auth(requests.Session(), METEOFRANCE_API_URL, METEOFRANCE_API_TOKEN)

    resp = auth.request("get", "places", params={"q": "montreal"})

    assert resp.status_code == 200


def test_auth_meteofrance():
    auth = AuthMeteofrance()

    resp = auth.request("get", "places", params={"q": "montreal"})

    assert resp.status_code == 200


def test_auth_without_params():
    auth = Auth(requests.Session(), "http://fakeurl.fake", "fake_token")

    with pytest.raises(requests.exceptions.ConnectionError):
        auth.request("get", "places")
