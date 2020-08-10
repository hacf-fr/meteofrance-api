# -*- coding: utf-8 -*-
"""Météo-France helpers."""
import math
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from pytz import timezone
from pytz import utc

from .const import ALERT_COLOR_LIST_EN
from .const import ALERT_COLOR_LIST_FR
from .const import ALERT_TYPE_LIST_EN
from .const import ALERT_TYPE_LIST_FR
from .const import COASTAL_DEPARTMENT_LIST
from .const import VALID_DEPARTMENT_LIST
from .model.place import Place


def get_warning_text_status_from_indice_color(
    int_color: int, lang: str = "fr"
) -> Optional[str]:
    """Convert the color code (in int) in readable text (Helper).

    Returned text is in French or English according to the lang parameter.
    """
    if lang == "fr":
        return ALERT_COLOR_LIST_FR[int_color]

    return ALERT_COLOR_LIST_EN[int_color]


def get_phenomenon_name_from_indice(
    int_phenomenon: int, lang: str = "fr"
) -> Optional[str]:
    """Convert the phenomenom code in readable text (Hepler).

    Returned text is in French or English according to the lang parameter.
    """
    if lang == "fr":
        return ALERT_TYPE_LIST_FR[int_phenomenon]

    return ALERT_TYPE_LIST_EN[int_phenomenon]


def is_coastal_department(department_number: str) -> bool:
    """Identify when a second bulletin is availabe for coastal risks (Helper)."""
    return department_number in COASTAL_DEPARTMENT_LIST


def is_valid_warning_department(department_number: str) -> bool:
    """Identify if there is a weather alert bulletin for this department (Helper).

    Weather alert buletins are available only for France métropole and Andorre.
    """
    return department_number in VALID_DEPARTMENT_LIST


def readeable_phenomenoms_dict(
    list_phenomenoms: List[Dict[str, int]], language: str = "fr"
) -> Dict[Optional[str], Optional[str]]:
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


def haversine(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """Compute distance in meters between to GPS coordinates using Harvesine formula.

    coord1 and coord2 are tuple with latitude and longitude in degrees.
    source: https://janakiev.com/blog/gps-points-distance-python/
    """
    radius = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )

    return 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def sort_places_versus_distance_from_coordinates(
    list_places: List[Place], gps_coord: Tuple[float, float]
) -> List[Place]:
    """Oder list of places according to the distance to a reference coordinates.

    gps_coordinates are in degrees.
    Note: this helper is compensating the bad results of the API. Results in the API
    are sorted but lot of case identified where it doesn't work (example: Montréal)
    """
    sorted_places = sorted(
        list_places,
        key=lambda x: haversine((float(x.latitude), float(x.longitude)), gps_coord),
    )
    return sorted_places


def timestamp_to_dateime_with_locale_tz(timestamp: int, local_tz: str) -> datetime:
    """Convert timestamp in datetime (Helper).

    The local timezone corresponding to the forecast location is used.
    """
    # convert timestamp in datetime with UTC timezone
    dt_utc = utc.localize(datetime.utcfromtimestamp(timestamp))
    # convert datetime to local timezone
    return dt_utc.astimezone(timezone(local_tz))
