import numpy as np
import pandas as pd

PATH_TO_DATA = "data"

def get_dataframe_for_states(df: pd.DataFrame, states: list):
    """Returns a filtered df if df.state contains `states`.
    Assumes that df contains `state` as a column.
    """
    return df[df.state.isin(states)]

def feature_to_radius(p: float):
    # This function is not determined yet and is subject to change,
    # and hence has limited testing. What is determined is that it 
    # has > 0 value.
    return max(np.log(p), 1)

if __name__ == "__main__":
    data_src = PATH_TO_DATA + "/ppv_state-district-geo-dataAug2021.csv"

    ppv_df = pd.read_csv(data_src)
    spk_states = [
        "Selangor",
        "W.P. Kuala Lumpur",
        "W.P. Putrajaya",
    ]
    spk_df = get_dataframe_for_states(ppv_df, spk_states)
    print(spk_df)