import streamlit as st
import pandas as pd
import numpy as np



CSV_FILE_STATS = 'LoadingStatistics.csv'
CSV_FILE_ROW_COUNTS = 'LoadingRowCounts.csv'


def load_data1(nrows):
    df = pd.read_csv(CSV_FILE_STATS, nrows=nrows, delimiter=";")
    df.columns = ['Source System','Source Description', 'Source File', 'Source File Pattern', \
        'Source File Type', 'Run Date', 'Load Step', 'Load Step Date Time', \
        'Load Step Start Date Time', 'Load Step End Date Time', 'Load Step Status', \
        'Load Step Exception', 'Load Step Exception Trace']

    return df



def load_data2(nrows):
    df = pd.read_csv(CSV_FILE_ROW_COUNTS, nrows=nrows, delimiter=";")
    df.columns = ['Sourcefile','Sourcefile Name', 'Sourcefile Type', \
        'Sourcefile Size', 'Run Date', 'Model Object', 'Model Attribute', \
        'Number Of Records Staged ', 'Number Of Records Processed ', 'Number Of Records Loaded ']

    return df

with st.spinner(text="Loading data, please wait..."):
    data = load_data1(100000)
    data2 = load_data2(100000)
st.success('Done!')

st.write(data)
st.write(data2)