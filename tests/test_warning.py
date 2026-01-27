"""Tests Météo-France module. Warning classes."""

from unittest.mock import Mock

import pytest

from meteofrance_api import MeteoFranceClient
from meteofrance_api.const import METEOFRANCE_API_URL

WARNING_COLOR_LIST = [1, 2, 3, 4]


def test_currentphenomenons(requests_mock: Mock) -> None:
    """Test basic weather alert results from API."""
    client = MeteoFranceClient()

    requests_mock.request(
        "get",
        f"{METEOFRANCE_API_URL}/v3/warning/currentphenomenons",
        json={
            "update_time": 1591279200,
            "end_validity_time": 1591365600,
            "domain_id": "32",
            "phenomenons_max_colors": [
                {"phenomenon_id": "6", "phenomenon_max_color_id": 1},
                {"phenomenon_id": "4", "phenomenon_max_color_id": 1},
                {"phenomenon_id": "5", "phenomenon_max_color_id": 3},
                {"phenomenon_id": "2", "phenomenon_max_color_id": 1},
                {"phenomenon_id": "1", "phenomenon_max_color_id": 1},
                {"phenomenon_id": "3", "phenomenon_max_color_id": 2},
            ],
        },
    )

    current_phenomenons = client.get_warning_current_phenomenons(domain="32", depth=1)

    assert isinstance(current_phenomenons.update_time, int)
    assert isinstance(current_phenomenons.end_validity_time, int)
    assert isinstance(current_phenomenons.domain_id, str)
    assert "phenomenon_id" in current_phenomenons.phenomenons_max_colors[0].keys()
    assert current_phenomenons.get_domain_max_color() == 3


def test_fulls() -> None:
    """Test advanced weather alert results from API."""
    client = MeteoFranceClient()

    warning_full = client.get_warning_full(domain="31")

    assert isinstance(warning_full.update_time, int)
    assert isinstance(warning_full.end_validity_time, int)
    assert isinstance(warning_full.domain_id, str)
    assert warning_full.domain_id == "31"
    assert warning_full.color_max in WARNING_COLOR_LIST
    assert (
        warning_full.timelaps[0]["timelaps_items"][0]["color_id"] in WARNING_COLOR_LIST
    )
    assert (
        warning_full.phenomenons_items[0]["phenomenon_max_color_id"]
        in WARNING_COLOR_LIST
    )


def test_thumbnail() -> None:
    """Test getting France status weather alert map."""
    client = MeteoFranceClient()

    thumbnail_url = client.get_warning_thumbnail()

    assert thumbnail_url == (
        "https://webservice.meteofrance.com/v3/warning/thumbnail"
        "?&token=__Wj7dVSTjV9YGu1guveLyDq0g7S7TfTjaHBTPTpO0kj8__&"
        "domain=france"
    )


@pytest.mark.parametrize(
    ("dep", "res_coastal", "res_avalanche"),
    [("13", True, False), ("32", False, False), ("74", False, True)],
)
def test_currentphenomenons_with_coastal_bulletin(
    dep: str, res_coastal: bool, res_avalanche: bool
) -> None:
    """Test getting a complete basic bulletin for coastal department."""
    client = MeteoFranceClient()

    current_phenomenons = client.get_warning_current_phenomenons(
        domain=dep, depth=1, with_coastal_bulletin=True
    )

    # has_avalanche_phenomenon = any(
    #     phenomenon["phenomenon_id"] == "8"
    #     for phenomenon in current_phenomenons.phenomenons_max_colors
    # )
    has_coastal_phenomenon = any(
        phenomenon["phenomenon_id"] == "9"
        for phenomenon in current_phenomenons.phenomenons_max_colors
    )

    # FIXME: ne fonctionne plus phenomenon_id 8 non trouvé: autre ID ?
    # https://meteofrance.com/meteo-montagne/alpes-du-nord/risques-avalanche
    # Bulletin avalanche : la saison est terminée, rendez-vous début novembre.
    # Pour les conditions en montagne pendant l'été, consultez les bulletins de
    # prévision Montagne départementaux
    # Haute-Savoie: 08 99 71 02 74
    # assert has_avalanche_phenomenon == res_avalanche
    assert has_coastal_phenomenon == res_coastal


@pytest.mark.parametrize(
    ("dep", "res_coastal", "res_avalanche"),
    [("13", True, False), ("32", False, False), ("74", False, True)],
)
def test_full_with_coastal_bulletin(
    dep: str, res_coastal: bool, res_avalanche: bool
) -> None:
    """Test getting a complete advanced bulletin for coastal department."""
    client = MeteoFranceClient()

    full_phenomenons = client.get_warning_full(domain=dep, with_coastal_bulletin=True)

    # has_avalanche_phenomenon = any(
    #     phenomenon["phenomenon_id"] == "8"
    #     for phenomenon in full_phenomenons.phenomenons_items
    # )
    has_coastal_phenomenon = any(
        phenomenon["phenomenon_id"] == "9"
        for phenomenon in full_phenomenons.phenomenons_items
    )

    # print("#"*100)
    # print(dep)
    # print(full_phenomenons.raw_data)
    # print(has_avalanche_phenomenon)
    # print(has_coastal_phenomenon)
    # print("#"*100)

    # FIXME: ne fonctionne plus phenomenon_id 8 non trouvé: autre ID ?
    # https://meteofrance.com/meteo-montagne/alpes-du-nord/risques-avalanche
    # Bulletin avalanche : la saison est terminée, rendez-vous début novembre.
    # Pour les conditions en montagne pendant l'été, consultez les bulletins de
    # prévision Montagne départementaux
    # Haute-Savoie: 08 99 71 02 74
    # assert has_avalanche_phenomenon == res_avalanche
    assert has_coastal_phenomenon == res_coastal
