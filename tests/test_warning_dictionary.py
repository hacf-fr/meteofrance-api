"""Tests for WarningDictionary class in the Météo-France module."""

import pytest

from meteofrance_api import MeteoFranceClient
from meteofrance_api.model import WarningDictionary
from meteofrance_api.model.dictionary import WarningDictionaryData


class TestWarningDictionary:
    """Tests for WarningDictionary class in the Météo-France module."""

    @pytest.fixture
    def sample_dictionary_data(self) -> WarningDictionaryData:
        """Provide sample data for WarningDictionary."""
        return {
            "phenomenons": [
                {"id": 1, "name": "Wind"},
                {"id": 2, "name": "Rain-flood"},
                {"id": 3, "name": "Thunderstorms"},
                {"id": 4, "name": "Flood"},
                {"id": 5, "name": "Snow-ice"},
                {"id": 6, "name": "Heat wave"},
                {"id": 7, "name": "Extreme Cold"},
                {"id": 8, "name": "Avalanche"},
                {"id": 9, "name": "Waves-flooding"},
            ],
            "colors": [
                {"id": 1, "level": 1, "name": "green", "hexaCode": "#31aa35"},
                {"id": 2, "level": 2, "name": "yellow", "hexaCode": "#fff600"},
                {"id": 3, "level": 3, "name": "orange", "hexaCode": "#ffb82b"},
                {"id": 4, "level": 4, "name": "red", "hexaCode": "#CC0000"},
            ],
        }

    def test_dictionary(self) -> None:
        """Test dictionary."""
        client = MeteoFranceClient()

        dictionary = client.get_warning_dictionary()

        assert isinstance(dictionary, WarningDictionary)
        color = dictionary.get_color_name_by_id(1)
        assert isinstance(color, str)
        phenomenon = dictionary.get_phenomenon_name_by_id(1)
        assert isinstance(phenomenon, str)

    def test_get_phenomenon_by_id(
        self, sample_dictionary_data: WarningDictionaryData
    ) -> None:
        """Test get_phenomenon_by_id method."""
        dictionary = WarningDictionary(sample_dictionary_data)

        phenomenon = dictionary.get_phenomenon_by_id(1)
        assert phenomenon == {"id": 1, "name": "Wind"}

        # Test for non-existing ID
        assert dictionary.get_phenomenon_by_id(99) is None

    def test_get_phenomenon_name_by_id(
        self, sample_dictionary_data: WarningDictionaryData
    ) -> None:
        """Test get_phenomenon_name_by_id method."""
        dictionary = WarningDictionary(sample_dictionary_data)

        name = dictionary.get_phenomenon_name_by_id(2)
        assert name == "Rain-flood"

        # Test for non-existing ID
        assert dictionary.get_phenomenon_name_by_id(99) is None

    def test_get_color_by_id(
        self, sample_dictionary_data: WarningDictionaryData
    ) -> None:
        """Test get_color_by_id method."""
        dictionary = WarningDictionary(sample_dictionary_data)

        color = dictionary.get_color_by_id(2)
        assert color == {"id": 2, "level": 2, "name": "yellow", "hexaCode": "#fff600"}

        # Test for non-existing ID
        assert dictionary.get_color_by_id(99) is None

    def test_get_color_name_by_id(
        self, sample_dictionary_data: WarningDictionaryData
    ) -> None:
        """Test get_color_name_by_id method."""
        dictionary = WarningDictionary(sample_dictionary_data)

        name = dictionary.get_color_name_by_id(1)
        assert name == "green"

        # Test for non-existing ID
        assert dictionary.get_color_name_by_id(99) is None
