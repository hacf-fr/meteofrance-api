# -*- coding: utf-8 -*-
"""
Meteo France weather forecast python API. Classes for weather alert.

For getting weather alerts in France and Andorre.
"""

from .const import (
    ALERT_COLOR_LIST_EN,
    ALERT_COLOR_LIST_FR,
    ALERT_TYPE_LIST_EN,
    ALERT_TYPE_LIST_FR,
    COASTAL_DEPARTMENT_LIST,
)

#
# Helpers
#


def get_text_status_from_indice_color(int_color: int, lang: str = "fr") -> str:
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
        ] = get_text_status_from_indice_color(
            phenomenom["phenomenon_max_color_id"], language
        )
    return readable_dict


#
# Classes
#


class CurrentPhenomenons(object):
    """Class to access the results of a `warning/currentPhenomenons` API command.

    For coastal department two bulletins are avalaible corresponding to two different
    domains.
    """

    def __init__(self, raw_data: dict):
        """Initialize a CurrentPhenomenons object."""
        self.raw_data = raw_data

    @property
    def update_time(self) -> int:
        """Return the update time of the phenomenoms."""
        return self.raw_data["update_time"]

    @property
    def end_validity_time(self) -> int:
        """Return the end of validty time of the phenomenoms."""
        return self.raw_data["end_validity_time"]

    @property
    def domain_id(self) -> str:
        """Return the domain ID of the phenomenoms."""
        return self.raw_data["domain_id"]

    @property
    def phenomenons_max_colors(self) -> list:
        """Return the list and colors of the phenomenoms."""
        return self.raw_data["phenomenons_max_colors"]

    def merge_with_coastal_phenomenons(
        self, coastal_phenomenoms: "CurrentPhenomenons"
    ) -> None:
        """Merge the classical phenomenoms bulleting with the coastal one."""
        # TODO: Add consitency check
        self.raw_data["phenomenons_max_colors"].extend(
            coastal_phenomenoms.phenomenons_max_colors
        )

    # def get_domain_max_color(self) -> str:
    #     """Helper to have the maximum level of alert of a given domain"""
    #     # TODO: warning nor working when there is a coastal department
    #     max_int_color = max(
    #         x["phenomenon_max_color_id"] for x in self.phenomenons_max_colors
    #     )
    #     return get_text_status_from_indice_color(max_int_color)


class Full(object):
    """This class allows to access the results of a `warning/full` API command.

    For a given domain we can access the maximum alert, a timelaps of the alert
    evolution for the next 24 hours, and a list of alerts.

    For coastal department two bulletins are avalaible corresponding to two different
    domains.
    """

    def __init__(self, raw_data: dict):
        """Initialize a Full object."""
        self.raw_data = raw_data

    @property
    def update_time(self) -> int:
        """Return the update time of the full bulletin."""
        return self.raw_data["update_time"]

    @property
    def end_validity_time(self) -> int:
        """Return the end of validty time of the full bulletin."""
        return self.raw_data["end_validity_time"]

    @property
    def domain_id(self) -> str:
        """Return the domain ID of the the full bulletin."""
        return self.raw_data["domain_id"]

    @property
    def color_max(self) -> int:
        """Return the color max of the domain."""
        return self.raw_data["color_max"]

    @property
    def timelaps(self) -> list:
        """Return the timelaps of each phenomenom for the domain."""
        return self.raw_data["timelaps"]

    @property
    def phenomenons_items(self) -> list:
        """Return the phenomenom list of the domain."""
        return self.raw_data["phenomenons_items"]

    def merge_with_coastal_phenomenons(self, coastal_phenomenoms: "Full") -> None:
        """Merge the classical phenomenoms bulleting with the coastal one."""
        # TODO: Add consitency check
        # TODO: Check if other data need to be merged

        # Merge color_max property
        self.raw_data["color_max"] = max(self.color_max, coastal_phenomenoms.color_max)

        # Merge timelaps
        self.raw_data["timelaps"].extend(coastal_phenomenoms.timelaps)

        # Merge phenomenons_items
        self.raw_data["phenomenons_items"].extend(coastal_phenomenoms.phenomenons_items)

    # TODO: check opportunity to complete class
