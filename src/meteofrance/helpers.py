# -*- coding: utf-8 -*-
"""Météo-France helpers."""

from .const import (
    ALERT_COLOR_LIST_EN,
    ALERT_COLOR_LIST_FR,
    ALERT_TYPE_LIST_EN,
    ALERT_TYPE_LIST_FR,
    COASTAL_DEPARTMENT_LIST,
)


def get_warning_text_status_from_indice_color(int_color: int, lang: str = "fr") -> str:
    """Convert the color code (in int) in readable text (Helper).

    Returned text is in French or English according to the lang parameter.
    """
    if lang == "fr":
        return ALERT_COLOR_LIST_FR[int_color]
    else:
        return ALERT_COLOR_LIST_EN[int_color]


def get_phenomenon_name_from_indice(int_phenomenon: int, lang: str = "fr") -> str:
    """Convert the phenomenom code in readable text (Hepler).

    Returned text is in French or English according to the lang parameter.
    """
    if lang == "fr":
        return ALERT_TYPE_LIST_FR[int_phenomenon]
    else:
        return ALERT_TYPE_LIST_EN[int_phenomenon]


def is_coastal_department(department_number: str) -> bool:
    """Iidentify when a second bulletin is availabe for coastal risks (Helper)."""
    result = False
    if department_number in COASTAL_DEPARTMENT_LIST:
        result = True
    return result


def readeable_phenomenoms_dict(list_phenomenoms: list, language: str = "fr") -> dict:
    """Create a dictionary with human readable keys and values (Helper)."""
    # Init empty dictionnary
    readable_dict = {}

    # Translate phenomenom name and alert level
    for phenomenom in list_phenomenoms:
        readable_dict[
            get_phenomenon_name_from_indice(phenomenom["phenomenon_id"], language)
        ] = get_warning_text_status_from_indice_color(
            phenomenom["phenomenon_max_color_id"], language
        )
    return readable_dict
