import streamlit as st
import pandas as pd
import numpy as np
from streamlit_timeline import st_timeline
import datetime as dt

st.set_page_config(layout="wide")

CSV_FILE_STATS = 'LoadingStatistics.csv'
CSV_FILE_ROW_COUNTS = 'LoadingRowCounts.csv'

#cur_time = dt.datetime.now()
cur_time = dt.datetime(2022, 1, 4, 1, 0, 0) #We're living in the past so that the first 10000 rows of data aren't too far away
cur_time

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


import plotly.express as px
import pandas as pd

df = pd.DataFrame([
    dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
    dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
    dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')
])

fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
st.write(fig.update_yaxes(autorange="reversed")) # otherwise tasks are listed from the bottom up



items = []

for i in range(10):
      items.append({"id": i, "content": data._get_value(i, 'Source File'), "start": data._get_value(i, 'Run Date')})



#items = [
#    {"id": 1, "content": "Hej", "start": "2022-10-20"},
#    {"id": 2, "content": "AAAAA", "start": "2022-10-09"},
#    {"id": 3, "content": "Seems sus", "start": "2022-10-18"},
#    {"id": 4, "content": "OH BABY", "start": "2022-10-16"},
#    {"id": 5, "content": "I bought many card", "start": "2022-10-25"},
#    {"id": 6, "content": "Nej vill inte", "start": "2022-10-27"},
#]

timeline = st_timeline(items, groups=[], options={}, height="300px")
st.subheader("Selected item")
st.write(timeline)



data['Run Date'] = pd.to_datetime(data['Run Date'])

masked_24_hours = data[(data['Run Date'] > (cur_time - dt.timedelta(days=1))) & (data['Run Date'] < cur_time)]
masked_48_hours = data[(data['Run Date'] > (cur_time - dt.timedelta(days=2))) & (data['Run Date'] < (cur_time - dt.timedelta(days=1)))]

data
masked_24_hours
masked_48_hours

st.write((masked_48_hours[['Load Step Status']].value_counts().get('Completed', 0)))
st.write((masked_24_hours[['Load Step Status']].value_counts().get('Completed', 0)))

st.write((masked_48_hours[['Load Step Status']].value_counts().get('Completed', 0) - masked_24_hours[['Load Step Status']].value_counts().get('Completed', 0)))


col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric(label="Completed", value=masked_24_hours[['Load Step Status']].value_counts().get('Completed', 0), delta=(int)(masked_48_hours[['Load Step Status']].value_counts().get('Completed', 0) - masked_24_hours[['Load Step Status']].value_counts().get('Completed', 0)))
col2.metric(label='Failed', value=masked_24_hours[['Load Step Status']].value_counts().get('Failed', 0), delta=0, delta_color='inverse')
col3.metric(label='Running', value=masked_24_hours[['Load Step Status']].value_counts().get('Running', 0), delta=0)
#col4.metric(label='Failed', value=filtered_data_time_sys[['Load Step Status']].value_counts()['Scheduled'], delta=0, delta_color='inverse')
#Icke filter, övriga och kalla dem för Waiting
#Kika på varför den dör om den inte hittar några fel

#if statDic == {}:
    #st.image('Images/Green.png')
#    st.success('All activeties have been completed!', icon="💯")
#elif 'Failed' in statDic.values():
    #st.image('Images/Red.png')
#    st.error('Some activeties have failed!', icon="🙈")
#else:
#    st.warning('Some activeties are still running!', icon="🏃")




st.write(data)
#st.write(data2)


