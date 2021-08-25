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

def plot_data(data: pd.DataFrame):
    data['point_radius_scaled'] = data['point_radius'] * scale_factor
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

data_url = "https://raw.githubusercontent.com/salfaris/yme-hack-2021/main/data/ppv_skp-geo-pop-data.csv"
df = fetch_load_data(data_url)

scale_factor = 500
df['point_radius'] = df.pop_density.apply(unitroid.generate_radius_for_row)
# df.drop(['pop_growth'], axis=1, inplace=True, errors='ignore')
# df.sort_values(by='pop_density', ascending=False, inplace=True)

st.write(df.drop(columns=['pop_density', 'pop_growth']))

plot_data(df)

def generate_n_centroid_for_district(df: pd.DataFrame, district_name: str, n: int):
    district_df = df[df.district == district_name]
    district_pop_density = district_df.pop_density.values[0]
    centroids = unitroid.n_centroid(district_df, n)
    centroids_pop_density = np.full((len(centroids), 1), district_pop_density)
    centroids_point_radius = unitroid.generate_radius_array(centroids_pop_density)
    st.write(centroids_point_radius.shape)
    st.write(centroids_point_radius)
    # return np.hstack((centroids, centroids_pop_density, centroids_point_radius))

res = generate_n_centroid_for_district(df, 'Gombak', 3)
st.write(res)