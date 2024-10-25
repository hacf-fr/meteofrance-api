"""Tests for meteofrance module. Exception classes."""

import pytest

from meteofrance_api.exceptions import MeteoFranceError


def test_meteofrance_exception() -> None:
    """Tests MeteoFranceError exception."""
    with pytest.raises(MeteoFranceError):
        # TODO test for coverage. To be update in the future.
        raise MeteoFranceError("Test Error")
