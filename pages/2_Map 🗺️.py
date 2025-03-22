import warnings
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

warnings.filterwarnings("ignore")

st.set_page_config(layout='wide')

st.title("Welcome to the Map 🗺️ page:")

st.write("""
        This page lets you view the Airbnb locations on the map for the chosen **Country** and **City** from the sidebar. There's a table below the map\
        which shows some info about the Airbnbs in that city, like total number of Airbnbs for each room type, mean prices for each room type in\
        that city, etc.
    """)

datasetURL = r"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/air-bnb-listings/exports/csv?lang=en&timezone=Asia%2FKolkata&use_labels=true&delimiter=%3B"

@st.cache_resource
def load_preprocessed_data():
    data = pd.read_csv(datasetURL, sep=';')
    data['Latitude'] = data['Coordinates'].apply(lambda x: x.split(',')[0]).astype(float)
    data['Longitude'] = data['Coordinates'].apply(lambda x: x.split(',')[1]).astype(float)
    data['Number of reviews per month'] = data['Number of reviews per month'].fillna(0)
    data = data.drop(['Room ID', 'Name', 'Host ID', 'Neighbourhood', 'Coordinates', 'Date last review', 'Updated Date', 'Location'], axis=1)
    return data

df = load_preprocessed_data()

with st.sidebar:
    countries = df['Country'].unique()
    country = st.selectbox(label='Country:', options=countries)
    city = st.selectbox(label='City:', options=df[df['Country'] == country]['City'].unique())

df1 = df[(df['Country'] == country) & (df['City'] == city)]

col_map1, col_map2, col_map3 = st.columns([1, 5, 1])

with col_map2:
    st.map(data=df1, latitude='Latitude', longitude='Longitude', use_container_width=False, width=1200, height=800)

    st.subheader(f"Summary Statistics of Airbnbs in {city}, {country}:")

    df1 = df[(df['Country'] == country) & (df['City'] == city)]
    d1 = dict(df1['Room type'].value_counts())
    d2 = dict(df1.groupby(by='Room type')['Room Price'].mean().apply(lambda x: round(x, 2)))
    d3 = dict(df1.groupby(by='Room type')['Room Price'].min().apply(lambda x: round(x, 2)))
    d4 = dict(df1.groupby(by='Room type')['Room Price'].max().apply(lambda x: round(x, 2)))

    count = pd.DataFrame(
        {
            "Room Type" : d1.keys(),
            "Count" : d1.values(),
            "Mean Room Price" : d2.values(),
            "Minimum Room Price" : d3.values(),
            "Maximum Room Price" : d4.values()
        }
    )
    count