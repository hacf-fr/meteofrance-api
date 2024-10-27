"""Dictionary Python model for the Météo-France REST API."""

from typing import List
from typing import Optional
from typing import TypedDict


class PhenomenonDictionaryEntry(TypedDict):
    """Represents a single meteorological phenomenon entry.

    Attributes:
        id: An integer representing the unique identifier of the phenomenon.
        name: A string representing the name of the phenomenon.
    """

    id: int
    name: str


class ColorDictionaryEntry(TypedDict):
    """Represents a single color entry used in meteorological warnings.

    Attributes:
        id: An integer representing the unique identifier of the color.
        level: An integer representing the severity level associated with the color.
        name: A string representing the name of the color.
        hexaCode: A string representing the hexadecimal code of the color.
    """

    id: int
    level: int
    name: str
    hexaCode: str  # noqa: N815


class WarningDictionaryData(TypedDict):
    """Structured data representing the meteorological dictionary.

    Attributes:
        phenomenons: A list of PhenomenonDictionaryEntry instances.
        colors: A list of ColorDictionaryEntry instances.
    """

    phenomenons: List[PhenomenonDictionaryEntry]
    colors: List[ColorDictionaryEntry]


class WarningDictionary:
    """A class to represent and manipulate the Météo-France meteorological dictionary data.

    Methods:
        get_phenomenon_name_by_id(phenomenon_id: int): Returns the name of the
        phenomenon for the given ID.
        get_color_name_by_id(color_id: int): Returns the name of the color for the given ID.
    """

    def __init__(self, raw_data: WarningDictionaryData) -> None:
        """Initializes the WarningDictionary with raw dictionary data.

        Args:
            raw_data: A dictionary representing the JSON response from the Météo-France API.
        """
        self.raw_data = raw_data

    def get_phenomenon_by_id(
        self, phenomenon_id: int
    ) -> Optional[PhenomenonDictionaryEntry]:
        """Retrieves a meteorological phenomenon based on its ID.

        Args:
            phenomenon_id: The ID of the meteorological phenomenon.

        Returns:
            The phenomenon if found, otherwise returns None.
        """
        for phenomenon in self.raw_data["phenomenons"]:
            if phenomenon["id"] == phenomenon_id:
                return phenomenon
        return None

    def get_phenomenon_name_by_id(self, phenomenon_id: int) -> Optional[str]:
        """Retrieves the name of a meteorological phenomenon based on its ID.

        Args:
            phenomenon_id: The ID of the meteorological phenomenon.

        Returns:
            The name of the phenomenon if found, otherwise returns None.
        """
        phenomenon = self.get_phenomenon_by_id(phenomenon_id)
        if phenomenon is not None:
            return phenomenon["name"]
        return None

    def get_color_by_id(self, color_id: int) -> Optional[ColorDictionaryEntry]:
        """Retrieves a warning color based on its ID.

        Args:
            color_id: The ID of the color.

        Returns:
            The the color object if found, otherwise returns None.
        """
        for color in self.raw_data["colors"]:
            if color["id"] == color_id:
                return color
        return None

    def get_color_name_by_id(self, color_id: int) -> Optional[str]:
        """Retrieves the name of a warning color based on its ID.

        Args:
            color_id: The ID of the color.

        Returns:
            The name of the color if found, otherwise returns None.
        """
        color = self.get_color_by_id(color_id)
        if color is not None:
            return color["name"]
        return None
