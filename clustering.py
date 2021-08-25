import numpy as np
import pandas as pd

def feature_to_radius(p: float):
    # This function is not determined yet and is subject to change,
    # and hence has limited testing. What is determined is that it 
    # has > 0 radius.
    return max(np.log(p), 1)