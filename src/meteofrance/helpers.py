# -*- coding: utf-8 -*-
"""Helpers to be used with the Météo-France REST API ."""
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

    Args:
        int_color: Color status in int. Value expected between 1 and 4.
        lang: Optional; If language is equal 'fr' (default value) results will
            be in French. All other value will give results in English.

    Returns:
        Color status in text. French or English according to the lang parameter.
    """
    if lang == "fr":
        return ALERT_COLOR_LIST_FR[int_color]

    return ALERT_COLOR_LIST_EN[int_color]


def get_phenomenon_name_from_indice(
    int_phenomenon: int, lang: str = "fr"
) -> Optional[str]:
    """Convert the phenomenom code in readable text (Hepler).

    Args:
        int_phenomenon: ID of the phenomenom in int. Value expected between 1 and 9.
        lang: Optional; If language is equal "fr" (default value) results will
            be in French. All other value will give results in English.

    Returns:
        Phenomenom in text. French or English according to the lang parameter.
    """
    if lang == "fr":
        return ALERT_TYPE_LIST_FR[int_phenomenon]

    return ALERT_TYPE_LIST_EN[int_phenomenon]


def is_coastal_department(department_number: str) -> bool:
    """Identify when a second bulletin is availabe for coastal risks (Helper).

    Args:
        department_number: Department number on 2 characters

    Returns:
        True if the department have an additional coastal bulletin. False otherwise.
    """
    return department_number in COASTAL_DEPARTMENT_LIST


def is_valid_warning_department(department_number: str) -> bool:
    """Identify if there is a weather alert bulletin for this department (Helper).

    Weather alert buletins are available only for metropolitan France and Andorre.

    Args:
        department_number: Department number on 2 characters.

    Returns:
        True if a department is metropolitan France or Andorre.
    """
    return department_number in VALID_DEPARTMENT_LIST


def readeable_phenomenoms_dict(
    list_phenomenoms: List[Dict[str, int]], language: str = "fr"
) -> Dict[Optional[str], Optional[str]]:
    """Create a dictionary with human readable keys and values (Helper).

    Args:
        list_phenomenoms: Dictionary with phenomenon ID and color code of status.
        language: Optional; If language is equal "fr" (default value) results will
            be in French. All other value will give results in English.

    Returns:
        Dictionary with keys and value human readable.
    """
    # Init empty dictionary
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

    source: https://janakiev.com/blog/gps-points-distance-python/

    Args:
        coord1: Tuple with latitude and longitude in degrees for first point
        coord2: Tuple with latitude and longitude in degrees for second point

    Returns:
        Distance in meters between the two points
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

    Note: this helper is compensating the bad results of the API. Results in the API
    are generally sorted, but lot of cases identified where the order is inconsistent
    (example: Montréal)

    Args:
        list_places: List of Place instances to be ordered
        gps_coord: Tuple with latitude and longitude in degrees for the reference point

    Returns:
        List of Place instances ordered by distance to the reference point (nearest
            first)
    """
    sorted_places = sorted(
        list_places,
        key=lambda x: haversine((float(x.latitude), float(x.longitude)), gps_coord),
    )
    return sorted_places


def timestamp_to_dateime_with_locale_tz(timestamp: int, local_tz: str) -> datetime:
    """Convert timestamp in datetime (Helper).

    Args:
        timestamp: Timestamp.
        local_tz: Name of the timezone to be used to convert the timestamp.

    Returns:
        Datetime instance corresponding to the timestamp with a timezone.
    """
    # convert timestamp in datetime with UTC timezone
    dt_utc = utc.localize(datetime.utcfromtimestamp(timestamp))
    # convert datetime to local timezone
    return dt_utc.astimezone(timezone(local_tz))
