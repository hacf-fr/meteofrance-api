"""Weather alert bulletin Python model for the Météo-France REST API.

For getting weather alerts in metropolitan France and Andorre.
"""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import TypedDict


# Define a custom type for items in the phenomenons_max_colors list
class PhenomenonMaxColor(TypedDict):
    """Describing a meteorological phenomenon and its maximum color code.

    Attributes:
        phenomenon_id (str): A unique identifier for the meteorological phenomenon.
                             This is kept as a string to match the format provided by
                             the API and could represent various types of weather
                             phenomena (e.g., storms, heavy rain, etc.).

        phenomenon_max_color_id (int): An integer representing the maximum alert color
                                       code associated with the phenomenon. The color
                                       codes typically indicate the severity or urgency
                                       of the weather-related alerts or warnings, with
                                       each color corresponding to a specific level of
                                       alert.
    """

    phenomenon_id: str
    phenomenon_max_color_id: int


class WarningCurrentPhenomenonsData(TypedDict):
    """Describing the data structure of CurrentPhenomenons object from the REST API."""

    update_time: int
    end_validity_time: int
    domain_id: str
    phenomenons_max_colors: List[PhenomenonMaxColor]


class WarningFullData(TypedDict):
    """Describing the data structure of full object from the REST API."""

    update_time: int
    end_validity_time: int
    domain_id: str
    color_max: int
    timelaps: List[Dict[str, Any]]
    phenomenons_items: List[PhenomenonMaxColor]
    advices: Optional[List[Dict[str, Any]]]
    consequences: Optional[List[Dict[str, Any]]]
    max_count_items: Any  # Didn't see any value yet
    comments: Dict[str, Any]
    text: Optional[Dict[str, Any]]
    text_avalanche: Any  # Didn't see any value yet


class CurrentPhenomenons:
    """Class to access the results of a `warning/currentPhenomenons` REST API request.

    For coastal department two bulletins are available corresponding to two different
    domains.

    Attributes:
        update_time: A timestamp (as integer) corresponding to the latest update of the
            phenomenons.
        end_validity_time: A timestamp (as integer) corresponding to expiration date of
            the phenomenons.
        domain_id: A string corresponding do the domain ID of the bulletin. Value is
            'France' or a department number.
        phenomenons_max_colors: A list of dictionaries with type of phenomenons and the
            current alert level.
    """

    def __init__(self, raw_data: WarningCurrentPhenomenonsData) -> None:
        """Initialize a CurrentPhenomenons object.

        Args:
            raw_data: A dictionary representing the JSON response from
                'warning/currentPhenomenons' REST API request. The structure is
                described by the WarningCurrentPhenomenonsData class.
        """
        self.raw_data = raw_data

    @property
    def update_time(self) -> int:
        """Return the update time of the phenomenons."""
        return self.raw_data["update_time"]

    @property
    def end_validity_time(self) -> int:
        """Return the end of validity time of the phenomenons."""
        return self.raw_data["end_validity_time"]

    @property
    def domain_id(self) -> str:
        """Return the domain ID of the phenomenons."""
        return self.raw_data["domain_id"]

    @property
    def phenomenons_max_colors(self) -> List[PhenomenonMaxColor]:
        """Return the list and colors of the phenomenons."""
        return self.raw_data["phenomenons_max_colors"]

    def merge_with_coastal_phenomenons(
        self, coastal_phenomenons: "CurrentPhenomenons"
    ) -> None:
        """Merge the classical phenomenons bulleting with the coastal one.

        Extend the phenomenons_max_colors property with the content of the coastal
        weather alert bulletin.

        Args:
            coastal_phenomenons: CurrentPhenomenons instance corresponding to the
                coastal weather alert bulletin.
        """
        # TODO: Add consistency check
        self.raw_data["phenomenons_max_colors"].extend(
            coastal_phenomenons.phenomenons_max_colors
        )

    def get_domain_max_color(self) -> int:
        """Get the maximum level of alert of a given domain (class helper).

        Returns:
            An integer corresponding to the status code representing the maximum alert.
        """
        max_int_color = max(
            x["phenomenon_max_color_id"] for x in self.phenomenons_max_colors
        )
        return max_int_color


class Full:
    """This class allows to access the results of a `warning/full` API command.

    For a given domain we can access the maximum alert, a timelaps of the alert
    evolution for the next 24 hours, and a list of alerts.

    For coastal department two bulletins are available corresponding to two different
    domains.

    Attributes:
        update_time: A timestamp (as integer) corresponding to the latest update of the
            phenomenons.
        end_validity_time: A timestamp (as integer) corresponding to expiration date of
            the phenomenons.
        domain_id: A string corresponding do the domain ID of the bulletin. Value is
            'France' or a department number.
        color_max: An integer representing the maximum alert level in the domain.
        timelaps: A list of dictionaries corresponding to the schedule of each
            phenomenons in the next 24 hours.
        phenomenons_items: list of dictionaries corresponding the alert level for each
            phenomenons type.
    """

    def __init__(self, raw_data: WarningFullData) -> None:
        """Initialize a Full object.

        Args:
            raw_data: A dictionary representing the JSON response from'warning/full'
                REST API request. The structure is described by the WarningFullData
                class.
        """
        self.raw_data = raw_data

    @property
    def update_time(self) -> int:
        """Return the update time of the full bulletin."""
        return self.raw_data["update_time"]

    @property
    def end_validity_time(self) -> int:
        """Return the end of validity time of the full bulletin."""
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
    def timelaps(self) -> List[Dict[str, Any]]:
        """Return the timelaps of each phenomenon for the domain."""
        return self.raw_data["timelaps"]

    @property
    def phenomenons_items(self) -> List[PhenomenonMaxColor]:
        """Return the phenomenon list of the domain."""
        return self.raw_data["phenomenons_items"]

    def merge_with_coastal_phenomenons(self, coastal_phenomenons: "Full") -> None:
        """Merge the classical phenomenon bulletin with the coastal one.

        Extend the color_max, timelaps and phenomenons_items properties with the content
            of the coastal weather alert bulletin.

        Args:
            coastal_phenomenons: Full instance corresponding to the coastal weather
                alert bulletin.
        """
        # TODO: Add consistency check
        # TODO: Check if other data need to be merged

        # Merge color_max property
        self.raw_data["color_max"] = max(self.color_max, coastal_phenomenons.color_max)

        # Merge timelaps
        self.raw_data["timelaps"].extend(coastal_phenomenons.timelaps)

        # Merge phenomenons_items
        self.raw_data["phenomenons_items"].extend(coastal_phenomenons.phenomenons_items)

    # TODO: check opportunity to complete class
