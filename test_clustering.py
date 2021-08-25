import pytest
from clustering import feature_to_radius

def test_greater_equal_one():
    assert feature_to_radius(0.01) > 0
    assert feature_to_radius(0.1) > 0
    assert feature_to_radius(0.5) > 0
    assert feature_to_radius(1) > 0
    assert feature_to_radius(2021) > 0