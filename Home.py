import streamlit as st
import pandas as pd
import numpy as np



CSV_FILE = 'LoadingStatistics.csv'


def load_data(nrows):
    df = pd.read_csv(CSV_FILE, nrows=nrows, delimiter=";")
    df.columns = ['Source System','Source Description', 'Source File', 'Source File Pattern', \
        'Source File Type', 'Run Date', 'Load Step', 'Load Step Date Time', \
        'Load Step Start Date Time', 'Load Step End Date Time', 'Load Step Status', \
        'Load Step Exception', 'Load Step Exception Trace']

    return df

with st.spinner(text="Loading data, please wait..."):
    data = load_data(100000)
st.success('Done!')

st.write(data)