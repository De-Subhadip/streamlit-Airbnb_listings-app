import warnings
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

warnings.filterwarnings("ignore")

st.set_page_config(layout='wide')

title_col1, title_col2, title_col3 = st.columns(3)

with title_col2:
    st.title(':rainbow[Airbnb Listings App: ]:house_with_garden:')
    
st.write(
    "Airbnb is a popular online marketplace that connects travelers with hosts offering unique accommodations, from apartments and houses to treehouses and tiny homes.\
    Founded in 2008, it has revolutionized the travel industry by providing affordable and diverse lodging options in cities worldwide.\
    With a user-friendly platform, Airbnb allows guests to book stays and experiences while enabling hosts to earn extra income by renting out their spaces.\
    However, it has also faced challenges, such as regulatory issues and concerns about its impact on local housing markets.\
    \n\nThis is a data visualization app of major Airbnb listings across some of the most popular tourist destinations worlwide.\
    The dataset used for this app consists of information about rooms listed on Airbnb.\
    Information come from the [open data website of Airbnb](http://insideairbnb.com/) which covered major cities worldwide.\
    For anonymizing data, precision of geo-coordinates point is 300m.\n\n**NOTE:** The dataset used for this app was last updated on August, 2020 as per the website."
    )

st.subheader('Dataset Description:')
st.write(""
    "The dataset consists of **17 columns** and about **1.41 million** rows. The column names are as follows: \n\n:blue-background[Room ID], :blue-background[Name], \
    :blue-background[Host ID], :blue-background[Neighbourhood], :blue-background[Room type], :blue-background[Room Price], :blue-background[Minimum nights], \
    :blue-background[Number of reviews], :blue-background[Date last review], :blue-background[Number of reviews per month], :blue-background[Rooms rent by the host], \
    :blue-background[Availability], :blue-background[Updated Date], :blue-background[City], :blue-background[Country], :blue-background[Coordinates], \
    :blue-background[Location]. \n\nThe data type and the number of values stored in each column is given in the table below:"
    )

datasetURL = r"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/air-bnb-listings/exports/csv?lang=en&timezone=Asia%2FKolkata&use_labels=true&delimiter=%3B"

@st.cache_resource
def load_data():
    data = pd.read_csv(datasetURL, sep=';')
    return data

df = load_data()

dfInfo = pd.DataFrame(
    {
        'Column Name' : [col for col in df.columns],
        'Non-null Count' : [(len(df) - df[col].isnull().sum()) for col in df.columns],
        'Data Type' : [str(df[col].dtype) for col in df.columns]
    }
)

df_col1, df_col2, df_col3 = st.columns([1, 3, 1])
with df_col2:
    st.dataframe(dfInfo, height=625)

if st.toggle(label="**Show Raw Data:**"):
    with st.spinner('Loading the dataset...'):
        st.dataframe(df, height=600)
        
st.markdown("[Link to Dataset](https://public.opendatasoft.com/explore/dataset/air-bnb-listings/export/?disjunctive.neighbourhood&disjunctive.column_10&disjunctive.city&location=2,13.38321,-0.05125&basemap=jawg.light)")
st.divider()