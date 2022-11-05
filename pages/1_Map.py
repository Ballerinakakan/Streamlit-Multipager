import streamlit as st
import pandas as pd
import numpy as np
import Home as hm

st.title('A map over all the pick-ups')

filter_time = st.slider('', 0, 23, 12)
st.subheader(f'Map of all pickups at {filter_time}:00')


filtered_data = hm.data[hm.data[hm.DATE_COLUMN].dt.hour == filter_time]
st.map(filtered_data)