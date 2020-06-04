# coding: utf-8
"""Tests for meteofrance module. Helpers."""

import pytest

from meteofrance.helpers import (
    get_phenomenon_name_from_indice,
    get_warning_text_status_from_indice_color,
    is_coastal_department,
    readeable_phenomenoms_dict,
)


def test_text_helpers_fr():
    """Test helpers to have readable alert type and alert level in French."""
    assert get_warning_text_status_from_indice_color(1) == "Vert"
    assert get_phenomenon_name_from_indice(2) == "Pluie-inondation"


def test_get_warning_text_status_from_indice_color_en():
    """Test helpers to have readable alert type and alert level in English."""
    assert get_warning_text_status_from_indice_color(4, "en") == "Red"
    assert get_phenomenon_name_from_indice(4, "en") == "Flood"


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
