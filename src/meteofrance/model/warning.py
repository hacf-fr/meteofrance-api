# -*- coding: utf-8 -*-
"""Météo-France weather forecast python API. Classes for weather alert.

For getting weather alerts in France and Andorre.
"""


class CurrentPhenomenons:
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

    def get_domain_max_color(self) -> int:
        """Get the maximum level of alert of a given domain (class helper)."""
        max_int_color = max(
            x["phenomenon_max_color_id"] for x in self.phenomenons_max_colors
        )
        return max_int_color


class Full:
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
