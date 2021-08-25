import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import unitroid

SEED = 44
COORD_COLS = ['latitude', 'longitude']

st.title("🚑 PPV On The Move")
st.markdown("PPV on the move, on the roof?")

# @st.cache
def fetch_load_data(url):
    data = pd.read_csv(url)
    return data

data_url = "https://raw.githubusercontent.com/salfaris/yme-hack-2021/main/data/ppv_skp-geo-pop-data.csv"
data = fetch_load_data(data_url)

# data['point_radius'] = data.pop_density.apply(unitroid.generate_radius_for_row)
scale_factor = 500
data['point_radius'] = unitroid.generate_radius_array(data.pop_density)
data['point_radius_scaled'] = data['point_radius'] * scale_factor
# data.drop(['pop_growth'], axis=1, inplace=True, errors='ignore')
# data.sort_values(by='pop_density', ascending=False, inplace=True)

st.write(data)

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

