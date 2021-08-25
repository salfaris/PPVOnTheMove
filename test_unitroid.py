import pytest
import numpy as np
import pandas as pd
from unitroid import (
    feature_to_radius, 
    n_centroid, 
    two_nearest_circle_point_centroid
)

@pytest.mark.parametrize("feature", [
    0.01, 0.1, 0.5, 1, 2021,
])
def test_greater_equal_one(feature):
    assert feature_to_radius(feature) > 0

even_len_df = pd.DataFrame({
    'latitude': np.arange(1, 11),
    'longitude': np.random.randn(10),
})
odd_len_df = pd.DataFrame({
    'latitude': np.arange(1, 10),
    'longitude': np.random.randn(9),
})

@pytest.mark.parametrize("df, n", [
    (even_len_df, 2),
    (odd_len_df, 2),
])
def test_is_numpy_array(df, n):
    assert isinstance(n_centroid(df, n), np.ndarray)

@pytest.mark.parametrize("df, n", [
    (even_len_df, 2),
    (even_len_df, 3),
    (odd_len_df, 4),
    (odd_len_df, 5),
])
def test_generate_exactly_n_centroids(df, n):
    assert len(n_centroid(df, n)) == n

@pytest.mark.parametrize("df, n", [
    (even_len_df, len(even_len_df)),
    (odd_len_df, len(odd_len_df)),
])  
def test_generate_centroids_less_than_equal_df(df, n):
    # The extreme case is where we do exactly len(df) splits of df
    # in which case len(n_centroid(df, n)) == len(df).
    assert len(n_centroid(df, n)) <= len(df)
    
def two_nearest_circle_point_centroid():
    x = np.array([0, 0], dtype=np.float64)
    y = np.array([4, -4], dtype=np.float64)
    radius_x = 3.0
    radius_y = 5.0
    
    assert (two_nearest_circle_point_centroid(
        x, y, radius_x, radius_y) == np.array([1.29289322 -1.29289322]))