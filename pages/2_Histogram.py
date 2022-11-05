import streamlit as st
import pandas as pd
import numpy as np
import Home as hm

st.title('A Histogram of the pick ups over time')
bar_data = np.histogram(hm.data[hm.DATE_COLUMN].dt.hour, bins=24, range=(0, 23))[0]
st.bar_chart(bar_data)