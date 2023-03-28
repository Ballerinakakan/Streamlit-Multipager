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



df['Run Date'] = pd.to_datetime(df['Run Date'])
filtered_data_time = df[ (df['Run Date'] >= start_time) & (df['Run Date'] <= end_time)]

filtered_data_time

reduceddf = filtered_data_time[['Source File', 'Run Date']]

timelinedf = reduceddf.drop_duplicates()
timelinedf
timelinedf = timelinedf.reset_index()
timelinedf = timelinedf[['Source File', 'Run Date']]

timelinedf

items = []

for index, row in timelinedf.iterrows():
      items.append({"id": index, "content": row['Source File'], "start": row['Run Date'].strftime("%Y-%m-%dT%H:%M:%S")})

items

#The format that it should be in
#items = [ {"id": 1, "content": "Hej", "start": "2022-10-20T12:00:00"} ]


timeline = st_timeline(items, groups=[], options={}, height="300px")
st.subheader("Selected item")
st.write(timeline)












#----------------------------------OLD ACTIVETIES-------------------------------------------------------------------

#df['Run Date'] = pd.to_datetime(df['Run Date'])
#filtered_data_time = df[ (df['Run Date'] >= start_time) & (df['Run Date'] <= end_time)]




actDic = {}
actdf = fildf[['Load Step', 'Run Date']].copy(deep=True)
for index, row in filtered_data_time.iterrows():
    actParsed = row['Load Step'].split('-')[0]
    if actParsed in actDic:
        actDic[actParsed] = actDic.get(actParsed) + 1
    else:
        actDic[actParsed] = 1
        graphdf = pd.DataFrame()



chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])




date_indexed_dataframe = actdf.copy(deep=True)
#date_indexed_dataframe


#pd.DataFrame.pivot(date_indexed_dataframe, index='Load Step Date Time', columns=[])


#date_indexed_dataframe.set_index('Run Date', inplace=True)
date_indexed_dataframe.rename(columns= {'Load Step':'LoadStep'}, inplace=True)




date_indexed_dataframe['LoadStep'] = date_indexed_dataframe.LoadStep.str.split('-').str[0]
date_indexed_dataframe
'lol'

final = date_indexed_dataframe.groupby(['LoadStep', 'Run Date'], as_index=False).size()
#st.write(counted)
#counteddf = counted.to_frame()
#'Converted!'
#counteddf
#st.write(counteddf)
#counteddf.rename(columns= {list(counteddf)[0] : 'Load Step'}, inplace= True)
#final
#asfasf = counteddf.unstack(level=0)
#st.write(type(asfasf))
#asfasf.rename(columns=asfasf.iloc[0])
#final = counteddf.reset_index()
final.rename(columns= {list(final)[2] : 'Count'}, inplace= True)
df = final.astype({'Count': 'int'})
final
'aaaaa'
finalfinal = final.pivot(index='Run Date', columns='LoadStep', values='Count')
finalfinal.fillna(0, inplace=True)
finalfinal
st.line_chart(finalfinal)

#pivoted = pd.DataFrame.pivot(date_indexed_dataframe, index='Run Date', columns='LoadStep')
#pivoted

#Try to make a chart of amount of times activity ran over time, where time is filtered by the filters at the top....
#this is gonna be hell to figure out. Could make it so {activity : [(time, runs), (time, runs)], activity2 : [(time: runs), (time, runs)]}
#could also make a dataframe with the colums as the activeties but not sure how to place time and runs to make it draw.

#Kika på lappen
#chart_data
#st.line_chart(chart_data)

#actdf
#actDic

#st.line_chart(date_indexed_dataframe)

    #act1    act2    act3
    #count   count   count
    #date    date    date