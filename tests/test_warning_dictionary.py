# coding: utf-8
"""Tests for WarningDictionary class in the Météo-France module."""
import pytest

from meteofrance_api import MeteoFranceClient
from meteofrance_api.model import WarningDictionary
from meteofrance_api.model.dictionary import WarningDisctionaryData


class TestWarningDictionary:
    """Tests for WarningDictionary class in the Météo-France module."""

    @pytest.fixture
    def sample_dictionary_data(self) -> WarningDisctionaryData:
        """Provide sample data for WarningDictionary."""
        return {
            "phenomenons": [{"id": 1, "name": "Wind"}, {"id": 2, "name": "Rain"}],
            "colors": [
                {"id": 1, "level": 1, "name": "Green", "hexaCode": "#00FF00"},
                {"id": 2, "level": 2, "name": "Yellow", "hexaCode": "#FFFF00"},
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
        self, sample_dictionary_data: WarningDisctionaryData
    ) -> None:
        """Test get_phenomenon_by_id method."""
        dictionary = WarningDictionary(sample_dictionary_data)

        phenomenon = dictionary.get_phenomenon_by_id(1)
        assert phenomenon == {"id": 1, "name": "Wind"}

        # Test for non-existing ID
        assert dictionary.get_phenomenon_by_id(99) is None

    def test_get_phenomenon_name_by_id(
        self, sample_dictionary_data: WarningDisctionaryData
    ) -> None:
        """Test get_phenomenon_name_by_id method."""
        dictionary = WarningDictionary(sample_dictionary_data)

        name = dictionary.get_phenomenon_name_by_id(2)
        assert name == "Rain"

        # Test for non-existing ID
        assert dictionary.get_phenomenon_name_by_id(99) is None

    def test_get_color_by_id(
        self, sample_dictionary_data: WarningDisctionaryData
    ) -> None:
        """Test get_color_by_id method."""
        dictionary = WarningDictionary(sample_dictionary_data)

        color = dictionary.get_color_by_id(2)
        assert color == {"id": 2, "level": 2, "name": "Yellow", "hexaCode": "#FFFF00"}

        # Test for non-existing ID
        assert dictionary.get_color_by_id(99) is None

    def test_get_color_name_by_id(
        self, sample_dictionary_data: WarningDisctionaryData
    ) -> None:
        """Test get_color_name_by_id method."""
        dictionary = WarningDictionary(sample_dictionary_data)

        name = dictionary.get_color_name_by_id(1)
        assert name == "Green"

        # Test for non-existing ID
        assert dictionary.get_color_name_by_id(99) is None
