import numpy as np
import pandas as pd

SEED = 44
PATH_TO_DATA = "data/"
COORD_COLS = ['latitude', 'longitude']

_data_src = PATH_TO_DATA + "ppv_skp-geo-pop-data.csv"
# spk_df = pd.read_csv(_data_src)

def feature_to_radius(pop_density: float):
    """The function defining the map: feature -> radius."""
    return np.log(pop_density)

def generate_radius_for_row(pop_density: float):
    np.random.seed(SEED)
    radius_mean_bound = feature_to_radius(pop_density)
    sigma = 1.5
    sampled_radius = sigma*np.random.randn(1) + radius_mean_bound
    return sampled_radius[0]

def generate_radius_array(pop_density_array: pd.Series, sigma: float = 1.5):
    np.random.seed(SEED)
    radius_mean_bound = feature_to_radius(pop_density_array)  # Vectorize
    sampled_radius = sigma*np.random.randn(len(pop_density_array)).reshape(-1, 1) + radius_mean_bound
    return sampled_radius

def n_centroid(df: pd.DataFrame, n: int):
    """Generates n centroids based on n splits of a uniformly
    shuffled DataFrame."""
    shuffled = df.sample(frac=1, random_state=SEED)
    splits = np.array_split(shuffled, n)
    
    centroids = []
    for split in splits:
        # Latitude, longitude values of the split.
        split_coords = split[COORD_COLS].values
        # NOTE :- Remind @salfaris, we need centroid to be computed 
        # midpoint between radii not center!
        centroid = split_coords.mean(axis=0) 
        centroids.append(centroid)
    
    return np.array(centroids)

# NOTE :- This function is unusable.
def two_nearest_circle_point_centroid(
    x: np.ndarray, # Length 2
    y: np.ndarray, # Length 2
    radius_x: float,
    radius_y: float
):
    """Calculates the centroid of the two points:
    1) The nearest point in the disc (x, radius_x) to y,
    2) The nearest point in the disc (y, radius_y) to x.
    """
    center_center_distance = np.sqrt(
        (x[0]-y[0])**2 + (x[1]-y[1])**2
    )
    t = radius_x - radius_y + center_center_distance
    t /= 2.0 * center_center_distance
    centroid = x + t*y
    return centroid