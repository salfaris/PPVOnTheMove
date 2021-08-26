import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import unitroid

from urllib.error import URLError

SEED = 44
COORD_COLS = ['latitude', 'longitude']
POINT_RADIUS_SCALE_FACTOR = 500
NUMERIC_ORIGINAL_COLS = ['latitude', 'longitude', 'pop_growth', 'pop_density']
DATA_COLS = ['state', 'district', 'ppv_name', 'latitude', 'longitude', 'pop_density', 'point_radius']
ALL_COLS = ['state', 'district', 'ppv_name', 'latitude', 'longitude', 'pop_growth', 'pop_density', 'point_radius', 'point_radius_scaled']

st.title("🚑 PPV On The Move")
st.markdown("*PPV on the move, instant vroom vroom with Unitroid*")
st.markdown("*Our [repo](https://github.com/salfaris/yme-hack-2021) for the hack.*")

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
    data = data.dropna()
    data[['latitude', 'longitude']] = data[['latitude', 'longitude']].apply(pd.to_numeric, errors='coerce')
    data = data.dropna()
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
    centroid_df = pd.DataFrame(arr, columns=ALL_COLS)
    centroid_df[ALL_COLS] = centroid_df[ALL_COLS].apply(pd.to_numeric, errors='ignore')
    return centroid_df

try:
    df = fetch_load_data()
    states = st.sidebar.multiselect(
        "Choose states", list(df.state.unique()), ["Selangor"]
    )
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    if not states:
        st.error("Please select at least one state.")
    else:
        states_df = df[df.state.isin(states)]
        states_df.reset_index(inplace=True, drop=True)
        st.write(states_df.drop(columns=['point_radius', 'point_radius_scaled']))
        st.write("Before Unitroid")
        plot_data(states_df)
        
        if st.sidebar.button("Apply Unitroid"):
            iter_nums = 51 if states != ['W.P. Kuala Lumpur'] else 1
            for i in range(iter_nums):
                status_text.text(f"{2*i}% Complete")
                progress_bar.progress(2*i)
                for state in states:
                    for district in states_df.district.unique():
                        centroids = generate_n_centroid_for_district(
                            states_df, state, district, 3)
                        states_df = pd.concat([states_df, centroids])
            states_df.reset_index(inplace=True, drop=True)
            st.write("After Unitroid")
            plot_data(states_df)
            
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )

st.markdown('## 🚑 What is PPV On The Move?')
st.markdown('*PPV On The Move* is an AI-driven project that utilise the *Uniform Centroid Algorithm (Unitroid)* that we developed to suggest strategic spots to place the PPV pop up centres. This project is purposed to help the government in improving the vaccination distribution that costs less time, with increased efficiency, backed by data and statistics.')

st.markdown('## :bulb: Our Motivation')
st.markdown('- :car: Increase reachability - Vaccines are for all and should be accessible by everyone from every nook and cranny.')
st.markdown('- :walking: Reduce overcrowding at centres - By having portable PPVs, people from various places would not need to gather at one small place and are able to practice social distancing. Ditch the long queues, and get vaccinated in an instant.')
st.markdown('- :triangular_ruler: A more reliable approach - Our approach is heavily backed up by data. This helps the government in making better decisions on where to open PPV to facilitate the recovery plan for Malaysia.')

st.markdown('## :clipboard: Our Methods')
st.markdown('This project was heavily relied on data. We decide to choose Selangor, W.P. Kuala Lumpur, and W.P. Putrajaya as point of reference for this project. ')
st.markdown('- :scissors: Data Scraping - We collected information of each PPV of the chosen states, categorised by districts scraped from the [JKJAV](https://www.vaksincovid.gov.my/ppv/) portal. With resources provided by [Department of Statistics Malaysia (DOSM)](https://www.dosm.gov.my/v1/index.php?r=column/cthree&menu_id=UmtzQ1pKZHBjY1hVZE95R3RnR0Y4QT09), we are able to obtain information of population density for each district in every state in Malaysia.' )
st.markdown('- :computer: Data Processing - We matched each PPV with its district, state, coordinates, and population density. This allows us to estimate the reachability of each existing PPV and picture them at the district and state level. With this piece of information, our own developed *Unitroid* algorithm can further suggest any region with less degree of reachability to the existing PPVs. ')

st.markdown('## :bulb: How Does Unitroid Work?')

st.markdown('As the name *Uniform Centroid* suggests, the Unitroid algorithm uses geometry to find potential PPV pop up centres by sampling current PPVs uniformly (i.e. in a uniform distribution fashion) and computing their centroid. Our hypothesis is that centroids arising in this way are suitable candidates to place pop up PPVs since it fills the PPV void in the state, allowing for better access to vaccines for those feeling burdened having to travel to current PPVs. Moreover, our experiments have shown that centroids drawn from the Unitroid algorithm gives rise to a natural path for PPV pop up centres to follow which reduces usage of resources.')