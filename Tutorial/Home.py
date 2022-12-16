import streamlit as st
import pandas as pd
import numpy as np

st.title('Welcome home my child!')

st.subheader('Its time to eat cinnamon pie')
'Please use the sidebar on the left to navigate to the different data presentations!'

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    #Loads Uber data and converts it into the pandas dataframe
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

#Load 10 000 rows of data into the dataframe.
with st.spinner(text='Loading data...'):
    data = load_data(10000)
st.success('Done!')

#notify the reader that the data was successfully loaded