import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import unitroid

from urllib.error import URLError

SEED = 44
COORD_COLS = ['latitude', 'longitude']
POINT_RADIUS_SCALE_FACTOR = 550
DATA_COLS = ['state', 'district', 'ppv_name', 'latitude', 'longitude', 'pop_density', 'point_radius']

st.title("🚑 PPV On The Move")
st.markdown("PPV on the move, on the roof?")

# @st.cache
def fetch_load_data():
    url = "https://raw.githubusercontent.com/salfaris/yme-hack-2021/main/data/ppv_skp-geo-pop-data.csv"
    df = pd.read_csv(url)
    df['point_radius'] = df.pop_density.apply(unitroid.generate_radius_for_row)
    df['point_radius_scaled'] = df['point_radius'] * POINT_RADIUS_SCALE_FACTOR
    return df

def handle_apply_algo_click():
    plot_data(states_df)

def plot_data(data: pd.DataFrame):
    init_view_lat = np.average(data['latitude'])
    init_view_lon = np.average(data['longitude'])
    init_zoom = 9
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=init_view_lat,
            longitude=init_view_lon,
            zoom=init_zoom,
            pitch=40
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=data,
                get_position=['longitude', 'latitude'],
                radius=1000,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=data,
                get_position=['longitude', 'latitude'],
                get_color='[200, 30, 0, 160]',
                get_radius=['point_radius_scaled'],
                opacity=0.2,
                stroked=True,
                filled=True
            ),
        ],
    ))
    
def generate_n_centroid_for_district(df: pd.DataFrame, state_name: str, district_name: str, n: int):
    district_df = df[df.district == district_name]
    district_pop_density = district_df.pop_density.values[0]
    district_pop_growth = district_df.pop_growth.values[0]
    centroids = unitroid.n_centroid(district_df, n)
    
    state_name = np.full((len(centroids), 1), state_name)
    district_name = np.full((len(centroids), 1), district_name)
    ppv_name = np.full((len(centroids), 1), 'new_centroid')
    
    pop_growth = np.full((len(centroids), 1), district_pop_growth)
    pop_density = np.full((len(centroids), 1), district_pop_density)
    point_radius = unitroid.generate_radius_array(pop_density)
    point_radius_scaled = point_radius * POINT_RADIUS_SCALE_FACTOR
    
    arr = np.hstack((state_name, district_name, ppv_name, centroids, pop_growth, pop_density, point_radius, point_radius_scaled))
    cols = ['state', 'district', 'ppv_name', 'latitude', 'longitude', 'pop_growth', 'pop_density', 'point_radius', 'point_radius_scaled']
    centroid_df = pd.DataFrame(arr, columns=cols)
    centroid_df[cols] = centroid_df[cols].apply(pd.to_numeric, errors='ignore')
    return centroid_df

try:
    df = fetch_load_data()
    states = st.sidebar.multiselect(
        "Choose states", list(df.state.unique()), ["Selangor"]
    )
    if not states:
        st.error("Please select at least one state.")
    else:
        states_df = df[df.state.isin(states)]
        states_df.reset_index(inplace=True, drop=True)
        st.write(states_df.drop(columns=['pop_density', 'pop_growth']))
        st.write("Before")
        plot_data(states_df)
        
        if st.sidebar.button("Apply Unitroid"):
            for state in states:
                for district in states_df.district.unique():
                    centroids = generate_n_centroid_for_district(
                        states_df, state, district, 3)
                    states_df = pd.concat([states_df, centroids])
            states_df.reset_index(inplace=True, drop=True)
            st.write("After")
            plot_data(states_df)
            
            
            
        
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )

# plot_data(df)

# res = generate_n_centroid_for_district(df, 'Selangor', 'Gombak', 3)
# data = pd.concat([df, res])