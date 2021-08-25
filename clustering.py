import numpy as np
import pandas as pd

SEED = 44
PATH_TO_DATA = "data/"
COORD_COLS = ['latitude', 'longitude']

_data_src = PATH_TO_DATA + "ppv_skp-geo-pop-data.csv"
spk_df = pd.read_csv(_data_src)

def feature_to_radius(feature: float):
    # This function is not determined yet and is subject to change,
    # and hence has limited testing. What is determined is that it 
    # has > 0 value.
    return max(np.log(feature), 1)

def n_centroid(df: pd.DataFrame, n: int):
    """Generates n centroids based on n splits of a uniformly
    shuffled DataFrame."""
    shuffled = df.sample(frac=1, random_state=SEED)
    splits = np.array_split(shuffled, n)
    
    centroids = []
    for split in splits:
        # Latitude, longitude values of the split.
        split_coords = split[COORD_COLS].values
        # Weightless centroid (as we are using mean).
        centroid = split_coords.mean(axis=0) 
        centroids.append(centroid)
    
    return np.array(centroids)
    
    