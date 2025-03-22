import warnings
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

warnings.filterwarnings("ignore")

st.set_page_config(layout='wide')

st.title('Welcome to the Plots 📊 Page:')

st.write("This page lets you visualize the Airbnb listings dataset for the purpose of EDA, with some interactive data visualizations. You can select the\
         **Country** of your choice from the sidebar to visualize the data for that country.")

datasetURL = r"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/air-bnb-listings/exports/csv?lang=en&timezone=Asia%2FKolkata&use_labels=true&delimiter=%3B"

@st.cache_data
def load_preprocessed_data():
    data = pd.read_csv(datasetURL, sep=';')
    data = data.drop(['Room ID', 'Name', 'Host ID', 'Neighbourhood', 'Coordinates', 'Date last review', 'Updated Date', 'Location'], axis=1)
    data['Number of reviews per month'] = data['Number of reviews per month'].fillna(0)
    return data

df = load_preprocessed_data()

with st.sidebar:
    country = st.selectbox(label='Choose a Country:', options=df['Country'].unique())

num_cols = [col for col in df.columns if df[col].dtype != object and 'ID' not in col and 'Date' not in col]

col_plot1, col_plot2 = st.columns(2)

df1 = df[(df['Country'] == country)]

with col_plot1:
    st.subheader(':red-background[Histogram:]')
    st.write(
        'This histogram shows the distribution of the chosen column for the chosen ***Country*** from the sidebar. You can also choose\
             to color the histogram based on the chosen ***Category***.'
        )
    col_histogram = st.selectbox(label = ':red[Choose a column for Histogram:]', options = num_cols, index=5)
    bins = st.slider(label=':red[Select the number of bins:]', min_value=10, max_value=1000, value=75, step=1)
    hist_cat = st.pills(label=':red[Choose a category for the histogram:]', options=[None, 'City', 'Room type'], default=None, key='hist_cat')
    fig1 = px.histogram(df1, x=col_histogram, nbins=bins, color=hist_cat, color_discrete_sequence=['indianred'] if hist_cat is None else None)
    histogram = st.plotly_chart(fig1)

with col_plot2:
    st.subheader(':blue-background[Box Plot:]')
    st.write(
        'This box plot shows the distribution of the chosen column for the chosen ***Country*** from the sidebar. You can also choose\
             to color the box plot based on the chosen ***Category***.'
        )
    col_histogram = st.selectbox(label = ':blue[Choose a column for Box Plot:]', options = num_cols, index=5)
    box_cat = st.pills(label=':blue[Choose a category for the box plot:]', options=[None, 'City', 'Room type'], default=None, key='box_cat')
    fig2 = px.box(df1, x=col_histogram, color=box_cat)
    histogram = st.plotly_chart(fig2)

col_plot3, col_plot4 = st.columns(2)

with col_plot3:
    st.subheader(':orange-background[Pie Chart of Cities:]')
    st.write('This pie chart shows the percentage of Airbnbs in each city for the chosen ***Country***.')
    city_counts = df1['City'].value_counts()
    city_counts_df = pd.DataFrame({"city" : dict(city_counts).keys(), "count" : dict(city_counts).values()})
    fig3 = px.pie(city_counts_df, values='count', names='city', color_discrete_sequence=px.colors.sequential.Aggrnyl)
    pie_chart1 = st.plotly_chart(fig3)

with col_plot4:
    st.subheader(':green-background[Pie Chart of Room Types:]')
    st.write('This pie chart shows the percentage of various Airbnb room types for the chosen ***Country***.')
    room_type_counts = df1['Room type'].value_counts()
    room_type_counts_df = pd.DataFrame({"room type" : dict(room_type_counts).keys(), "count" : dict(room_type_counts).values()})
    fig4 = px.pie(room_type_counts_df, values='count', names='room type', color_discrete_sequence=px.colors.sequential.RdBu)
    pie_chart2 = st.plotly_chart(fig4)
