# This is the intro to streamlit done for learning purposes before continuing on to do the cool multipage app tutorial. Then finaly the grand app shall be made!

import streamlit as st
import pandas as pd
import numpy as np

st.title("Uber pick ups NYC")

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



#Create a text element
data_load_state = st.text('Loading data...')
#Load 10 000 rows of data into the dataframe.
data = load_data(10000)
#notify the reader that the data was successfully loaded
data_load_state = st.text('Success!')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
#Creates a histogram to display how many pickups happen at each hour of the day using numpy 
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
#Draws the histogram on the app
st.bar_chart(hist_values)

#Next "Plot data on a map", 1 hour done week 44, 9 to go c:


hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)