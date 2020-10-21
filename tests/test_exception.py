# coding: utf-8
"""Tests for meteofrance module. Exception classes."""
import pytest

from meteofrance_api.exceptions import MeteoFranceException


def test_meteofrance_exception() -> None:
    """Tests MeteoFranceException excetion."""
    with pytest.raises(MeteoFranceException):
        # TODO test for coverage. To be update in the future.
        raise MeteoFranceException("Test Error")
