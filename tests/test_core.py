"""Tests of the core functionalities."""
import pytest
from rlay import square

@pytest.mark.parametrize("value", list(range(100)))
def test_square(value: int):
    assert square(value) == value**2
