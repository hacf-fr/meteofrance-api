# coding: utf-8
"""Tests for meteofrance module. Warning classes."""
import pytest

from meteofrance.auth import MeteoFranceAuth
from meteofrance.client import MeteoFranceClient
from meteofrance.warning import (
    get_phenomenon_name_from_indice,
    get_text_status_from_indice_color,
    is_coastal_department,
    readeable_phenomenoms_dict,
)

WARNING_COLOR_LIST = [1, 2, 3, 4]


def test_currentphenomenons():
    """Test basic weather alert results from API."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

    current_phenomenoms = client.get_warning_current_phenomenoms(
        domain="france", depth=1
    )

    assert [
        type(current_phenomenoms.update_time),
        type(current_phenomenoms.end_validity_time),
        type(current_phenomenoms.domain_id),
        "phenomenon_id" in current_phenomenoms.phenomenons_max_colors[0].keys(),
    ] == [int, int, str, True]


def test_fulls():
    """Test advanced weather alert results from API."""
    auth = MeteoFranceAuth()
    client = MeteoFranceClient(auth)

    timelaps_list = client.get_warning_full(domain="31")

    assert [
        type(timelaps_list.update_time),
        type(timelaps_list.end_validity_time),
        type(timelaps_list.domain_id),
        timelaps_list.domain_id,
        timelaps_list.color_max in WARNING_COLOR_LIST,
        timelaps_list.timelaps[0]["timelaps_items"][0]["color_id"]
        in WARNING_COLOR_LIST,
        timelaps_list.phenomenons_items[0]["phenomenon_max_color_id"]
        in WARNING_COLOR_LIST,
    ] == [int, int, str, "31", True, True, True]


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


def test_text_helpers_fr():
    """Test helpers to have readable alert type and alert level in French."""
    assert [
        get_text_status_from_indice_color(1),
        get_phenomenon_name_from_indice(2),
    ] == ["Vert", "Pluie-inondation"]


def test_get_text_status_from_indice_color_en():
    """Test helpers to have readable alert type and alert level in English."""
    assert [
        get_text_status_from_indice_color(4, "en"),
        get_phenomenon_name_from_indice(4, "en"),
    ] == ["Red", "Flood"]


@pytest.mark.parametrize("dep, res", [("03", False), ("06", True), ("2B", True)])
def test_is_coastal_department(dep, res):
    """Test the helper checking if an additional coastal departement bulletin exist."""
    assert is_coastal_department(dep) == res


def test_readeable_phenomenoms_dict():
    """Test the helper constructing a human readable dictionary for phenomenom."""
    api_list = [
        {"phenomenon_id": 4, "phenomenon_max_color_id": 1},
        {"phenomenon_id": 5, "phenomenon_max_color_id": 1},
        {"phenomenon_id": 3, "phenomenon_max_color_id": 2},
        {"phenomenon_id": 2, "phenomenon_max_color_id": 1},
        {"phenomenon_id": 1, "phenomenon_max_color_id": 3},
    ]
    expected_dictionary = {
        "Inondation": "Vert",
        "Neige-verglas": "Vert",
        "Pluie-inondation": "Vert",
        "Orages": "Jaune",
        "Vent violent": "Orange",
    }

    assert readeable_phenomenoms_dict(api_list) == expected_dictionary


@pytest.mark.parametrize("dep, res", [("13", True), ("32", False)])
def test_currentphenomenons_with_coastal_bulletint(dep, res):
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
