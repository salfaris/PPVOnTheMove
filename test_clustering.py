import pytest
import numpy as np
import pandas as pd
from clustering import feature_to_radius, n_centroid

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
    
@pytest.mark.parametrize("feature", [
    0.01, 0.1, 0.5, 1, 2021,
])
def test_greater_equal_one(feature):
    assert feature_to_radius(feature) > 0