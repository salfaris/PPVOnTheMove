import pandas as pd

def get_dataframe_for_states(df: pd.DataFrame, states: list):
    """Returns a filtered df if df.state contains `states`.
    Assumes that df contains `state` as a column.
    
    Example
    -------
    >>> df = ...    
    >>> spk_states = [
             "Selangor",
             "W.P. Kuala Lumpur",
             "W.P. Putrajaya",
         ]
    >>> states_df = get_dataframe_for_states(df, spk_states)
    """
    return df[df.state.isin(states)]