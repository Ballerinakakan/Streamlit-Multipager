import streamlit as st
import pandas as pd
import numpy as np
import time as tm
import datetime as dt
import dateutil.parser as dp
from streamlit_timeline import st_timeline
import Home as hm


STEP_STATUSES = ['Scheduled', 'Inisiated/Queued', 'Running', 'Restarted', 'Completed', 'Failed', 'Unknown']

#cur_time = dt.datetime.now()
cur_time = dt.datetime(2022, 2, 3, 1, 0, 0) #We're living in the past so that the first 10000 rows of data aren't too far away
df = hm.data


#selected_source_system = st.selectbox('Select source systems:', \
#    options=df['Source System'].unique())


#Below is to filter to only look at one source file at a time
#selected_source_file = st.selectbox('Select source File:', \
#    options= df[(df['Source System'] == selected_source_system)]['Source File'].unique())

#fildf = df[df['Source System'] == selected_source_system][df['Source File'] == selected_source_file]
#fildf

#old_time = cur_time - dt.timedelta(days=30)
old_time = cur_time - dt.timedelta(days=180)

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(label="Start date", value=cur_time - dt.timedelta(days=1),max_value=cur_time, min_value= old_time)
    start_hour = st.time_input(label="Start time", value=cur_time - dt.timedelta(days=1))

with col2:
    end_date = st.date_input(label="End date", value=cur_time,max_value=cur_time, min_value= old_time)
    end_hour = st.time_input(label="End time", value=cur_time)

start_time = dt.datetime.combine(start_date, start_hour)
end_time = dt.datetime.combine(end_date, end_hour)



#Converts the timedate string into pandas Timestamp and then Forces it into being in pyTimedate instead
df['Run Date'] = pd.to_datetime(df['Run Date'])
arr_date = df['Run Date'].dt.to_pydatetime()
df['Run Date'] = pd.Series(arr_date, dtype="object")





filtered_data_time = df[ (df['Run Date'] >= start_time) & (df['Run Date'] <= end_time)]

#filtered_data_time

reduceddf = filtered_data_time[['Source File', 'Run Date']]

timelinedf = reduceddf.drop_duplicates()
timelinedf = timelinedf.reset_index()
timelinedf = timelinedf[['Source File', 'Run Date']]

#timelinedf

items = []

for index, row in timelinedf.iterrows():
      items.append({"id": index, "content": row['Source File'], "start": row['Run Date'].strftime("%Y-%m-%dT%H:%M:%S")})

#items

#The format that it should be in
#items = [ {"id": 1, "content": "Hej", "start": "2022-10-20T12:00:00"} ]


timeline = st_timeline(items, groups=[], options={}, height="700px")
#st.subheader("Selected item")
#st.write(timeline)


#st.write(type(t))
#st.write(type(timelinedf._get_value(0, 'Run Date')))

#st.write((t))
#st.write((timelinedf._get_value(0, 'Run Date')))


#st.write((t) == (timelinedf._get_value(0, 'Run Date')))

if timeline:
    t = dt.datetime.strptime(timeline["start"], "%Y-%m-%dT%H:%M:%S")
    filtereddf = filtered_data_time[ (filtered_data_time['Source File'] == timeline["content"]) & (filtered_data_time['Run Date'] == t)]
    filtereddf





st.write("-------------------------------------------------------------------------------------------")


