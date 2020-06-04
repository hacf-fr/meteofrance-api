# coding: utf-8
"""Tests for meteofrance module. Warning classes."""
import pytest

from meteofrance.auth import MeteoFranceAuth
from meteofrance.client import MeteoFranceClient

WARNING_COLOR_LIST = [1, 2, 3, 4]


def test_currentphenomenons():
    """Test basic weather alert results from API."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

    current_phenomenoms = client.get_warning_current_phenomenoms(
        domain="france", depth=1
    )

    assert type(current_phenomenoms.update_time) == int
    assert type(current_phenomenoms.end_validity_time) == int
    assert type(current_phenomenoms.domain_id) == str
    assert "phenomenon_id" in current_phenomenoms.phenomenons_max_colors[0].keys()


def test_fulls():
    """Test advanced weather alert results from API."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

    warning_full = client.get_warning_full(domain="31")

    assert type(warning_full.update_time) == int
    assert type(warning_full.end_validity_time) == int
    assert type(warning_full.domain_id) == str
    assert warning_full.domain_id == "31"
    assert warning_full.color_max in WARNING_COLOR_LIST
    assert (
        warning_full.timelaps[0]["timelaps_items"][0]["color_id"] in WARNING_COLOR_LIST
    )
    assert (
        warning_full.phenomenons_items[0]["phenomenon_max_color_id"]
        in WARNING_COLOR_LIST
    )


def test_thumbnail():
    """Test getting France status weather alert map."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

    thumbnail_url = client.get_warning_thumbnail()

    assert thumbnail_url == (
        "http://webservice.meteofrance.com/warning/thumbnail"
        "?&token=__Wj7dVSTjV9YGu1guveLyDq0g7S7TfTjaHBTPTpO0kj8__&"
        "domain=france"
    )


@pytest.mark.parametrize("dep, res", [("13", True), ("32", False)])
def test_currentphenomenons_with_coastal_bulletin(dep, res):
    """Test getting a complete basic bulletin for coastal department."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

    current_phenomenoms = client.get_warning_current_phenomenoms(
        domain=dep, depth=1, with_costal_bulletin=True
    )
    has_coastal_phenomenom = any(
        phenomenom["phenomenon_id"] == 9
        for phenomenom in current_phenomenoms.phenomenons_max_colors
    )
    assert has_coastal_phenomenom == res


@pytest.mark.parametrize("dep, res", [("13", True), ("32", False)])
def test_full_with_coastal_bulletint(dep, res):
    """Test getting a complete advanced bulletin for coastal department."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

    full_phenomenoms = client.get_warning_full(domain=dep, with_costal_bulletin=True)

    has_coastal_phenomenom = any(
        phenomenom["phenomenon_id"] == 9
        for phenomenom in full_phenomenoms.phenomenons_items
    )
    assert has_coastal_phenomenom == res
