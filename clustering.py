import numpy as np
import pandas as pd

PATH_TO_DATA = "data"

def feature_to_radius(p: float):
    # This function is not determined yet and is subject to change,
    # and hence has limited testing. What is determined is that it 
    # has > 0 value.
    return max(np.log(p), 1)

if __name__ == "__main__":
    data_src = PATH_TO_DATA + "/ppv_skp-geo-pop-data.csv"

    spk_df = pd.read_csv(data_src)
    print(spk_df)