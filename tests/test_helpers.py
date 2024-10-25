"""Tests for meteofrance module. Helpers."""

from typing import List

import pytest

from meteofrance_api.helpers import get_phenomenon_name_from_indice
from meteofrance_api.helpers import get_warning_text_status_from_indice_color
from meteofrance_api.helpers import is_coastal_department
from meteofrance_api.helpers import is_valid_warning_department
from meteofrance_api.helpers import readeable_phenomenoms_dict
from meteofrance_api.helpers import sort_places_versus_distance_from_coordinates
from meteofrance_api.model import Place
from meteofrance_api.model.place import PlaceData
from meteofrance_api.model.warning import PhenomenonMaxColor


def test_text_helpers_fr() -> None:
    """Test helpers to have readable alert type and alert level in French."""
    assert get_warning_text_status_from_indice_color(1) == "Vert"
    assert get_phenomenon_name_from_indice("2") == "Pluie-inondation"


def test_get_warning_text_status_from_indice_color_en() -> None:
    """Test helpers to have readable alert type and alert level in English."""
    assert get_warning_text_status_from_indice_color(4, "en") == "Red"
    assert get_phenomenon_name_from_indice("4", "en") == "Flood"


@pytest.mark.parametrize(
    "dep, res",
    [
        ("03", False),
        ("06", True),
        ("69", False),
        ("74", False),
        ("98", False),
        ("2B", True),
    ],
)
def test_is_coastal_department(dep: str, res: bool) -> None:
    """Test the helper checking if an additional coastal departement bulletin exist."""
    assert is_coastal_department(dep) == res


@pytest.mark.parametrize(
    "dep, res",
    [
        ("03", True),
        ("69", True),
        ("74", True),
        ("98", False),
        ("2B", True),
    ],
)
def test_is_valid_warning_department(dep: str, res: bool) -> None:
    """Test the helper checking if departent has a weather alert bulletin."""
    assert is_valid_warning_department(dep) == res


def test_readeable_phenomenoms_dict() -> None:
    """Test the helper constructing a human readable dictionary for phenomenom."""
    api_list = [
        PhenomenonMaxColor(phenomenon_id="4", phenomenon_max_color_id=1),
        PhenomenonMaxColor(phenomenon_id="5", phenomenon_max_color_id=1),
        PhenomenonMaxColor(phenomenon_id="3", phenomenon_max_color_id=2),
        PhenomenonMaxColor(phenomenon_id="2", phenomenon_max_color_id=1),
        PhenomenonMaxColor(phenomenon_id="1", phenomenon_max_color_id=3),
    ]

    expected_dictionary = {
        "Inondation": "Vert",
        "Neige-verglas": "Vert",
        "Pluie-inondation": "Vert",
        "Orages": "Jaune",
        "Vent violent": "Orange",
    }

    assert readeable_phenomenoms_dict(api_list) == expected_dictionary


def test_sort_places_versus_distance_from_coordinates() -> None:
    """Test the helper to order the Places list return by the search."""
    json_places: List[PlaceData] = [
        {
            "insee": "11254",
            "name": "Montréal",
            "lat": 43.2,
            "lon": 2.14083,
            "country": "FR",
            "admin": "Languedoc-Roussillon",
            "admin2": "11",
            "postCode": "11290",
        },
        {
            "insee": "32290",
            "name": "Montréal",
            "lat": 43.95,
            "lon": 0.20222,
            "country": "FR",
            "admin": "Midi-Pyrénées",
            "admin2": "32",
            "postCode": "32250",
        },
        {
            "insee": "07162",
            "name": "Montréal",
            "lat": 44.5284,
            "lon": 4.2938,
            "country": "FR",
            "admin": "Rhône-Alpes",
            "admin2": "07",
            "postCode": "07110",
        },
        {
            "insee": "89267",
            "name": "Montréal",
            "lat": 47.54222,
            "lon": 4.03611,
            "country": "FR",
            "admin": "Bourgogne",
            "admin2": "89",
            "postCode": "89420",
        },
        {
            "insee": "null",
            "name": "Montréal",
            "lat": 45.50884,
            "lon": -73.58781,
            "country": "CA",
            "admin": "Quebec",
            "admin2": "06",
            "postCode": "null",
        },
        {
            "insee": "01265",
            "name": "Montréal-la-Cluse",
            "lat": 46.1871,
            "lon": 5.5709,
            "country": "FR",
            "admin": "Rhône-Alpes",
            "admin2": "01",
            "postCode": "01460",
        },
        {
            "insee": "26209",
            "name": "Montréal-les-Sources",
            "lat": 44.40139,
            "lon": 5.3,
            "country": "FR",
            "admin": "Rhône-Alpes",
            "admin2": "26",
            "postCode": "26510",
        },
        {
            "insee": "null",
            "name": "Montréal-Ouest",
            "lat": 45.45286,
            "lon": -73.64918,
            "country": "CA",
            "admin": "Quebec",
            "admin2": "null",
            "postCode": "null",
        },
        {
            "insee": "null",
            "name": "Montréal-Est",
            "lat": 45.63202,
            "lon": -73.5075,
            "country": "CA",
            "admin": "Quebec",
            "admin2": "null",
            "postCode": "null",
        },
        {
            "insee": "11432",
            "name": "Villeneuve-lès-Montréal",
            "lat": 43.18,
            "lon": 2.11139,
            "country": "FR",
            "admin": "Languedoc-Roussillon",
            "admin2": "11",
            "postCode": "11290",
        },
        {
            "insee": "null",
            "name": "Montereale Valcellina",
            "lat": 46.1511,
            "lon": 12.64771,
            "country": "IT",
            "admin": "Friuli Venezia Giulia",
            "admin2": "PN",
            "postCode": "null",
        },
        {
            "insee": "null",
            "name": "Mont-ral",
            "lat": 41.28333,
            "lon": 1.1,
            "country": "ES",
            "admin": "Catalonia",
            "admin2": "T",
            "postCode": "null",
        },
    ]
    list_places = [Place(place_data) for place_data in json_places]

    # Sort Places by distance from Auch (32) coordinates.
    list_places_ordered = sort_places_versus_distance_from_coordinates(
        list_places, (43.64528, 0.58861)
    )

    # first one should be in Gers
    assert list_places_ordered[0].admin2 == "32"
    # second in Aude
    assert list_places_ordered[1].admin2 == "11"
