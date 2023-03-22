import streamlit as st
import pandas as pd
import numpy as np
import time as tm
import datetime as dt
import dateutil.parser as dp
import Home as hm

#st.set_page_config(layout="wide")

STEP_STATUSES = ['Initiated/Queued', 'Scheduled', 'Running', 'Restarted', 'Completed', 'Failed', 'Unknown']



#current_time = tm.localtime

#appointment = st.slider(
#    "Schedule your appointment:",
#    value=(time(11, 30), time(12, 45)))
#st.write("You're scheduled for:", appointment)

#Above is example code of an interval range slider that could be used for this to filter
#between two specific times. Check if this would be a better solution

#cur_time = dt.datetime.now()
cur_time = dt.datetime(2022, 1, 4, 1, 0, 0) #We're living in the past so that the first 10000 rows of data aren't too far away
df = hm.data

# Kan man få med sig filter mellan undersidor
#cur_time
#df['Run Date'][1]

#st.write(dp.isoparse(df['Run Date'][1]))


filtered_source_systems = st.multiselect('Select source systems:', \
    options=df['Source System'].unique(), default=df['Source System'].unique() )

old_time = cur_time - dt.timedelta(days=30)

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(label="Start date", value=cur_time - dt.timedelta(days=1),max_value=cur_time, min_value= old_time)
    start_hour = st.time_input(label="Start time", value=cur_time - dt.timedelta(days=1))

with col2:
    end_date = st.date_input(label="End date", value=cur_time,max_value=cur_time, min_value= old_time)
    end_hour = st.time_input(label="End time", value=cur_time)

start_time = dt.datetime.combine(start_date, start_hour)
end_time = dt.datetime.combine(end_date, end_hour)

#days = st.slider('Days:', min_value=1, max_value=7, value=1)
#hours = st.slider('Time:', min_value=0, max_value=120, value=24)
#search_time = cur_time - dt.timedelta(hours=hours)

df['Run Date'] = pd.to_datetime(df['Run Date'])
filtered_data_time = df[ (df['Run Date'] >= start_time) & (df['Run Date'] <= end_time)]
filtered_data_time_sys = filtered_data_time[filtered_data_time['Source System'].isin(filtered_source_systems)]

actDic = {}
statDic ={}
actdf = filtered_data_time[['Load Step', 'Load Step Status']].copy(deep=True)
for index, row in filtered_data_time.iterrows():
    actParsed = row['Load Step'].split('-')[0]
    if actParsed in actDic:
        actDic[actParsed] = actDic.get(actParsed) + 1
    else:
        actDic[actParsed] = 1

    if row['Load Step Status'] != 'Completed':
        statDic[index] = row['Load Step Status']


#filtered_data_time_sys

st.write(filtered_data_time_sys[['Load Step Status']].value_counts()['Completed'])

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric(label="Completed", value=filtered_data_time_sys[['Load Step Status']].value_counts().get('Completed', 0), delta=0)
col2.metric(label='Failed', value=filtered_data_time_sys[['Load Step Status']].value_counts().get('Failed', 0), delta=0, delta_color='inverse')
col3.metric(label='Running', value=filtered_data_time_sys[['Load Step Status']].value_counts().get('Running', 0), delta=0)
#col4.metric(label='Failed', value=filtered_data_time_sys[['Load Step Status']].value_counts()['Scheduled'], delta=0, delta_color='inverse')
#Icke filter, övriga och kalla dem för Waiting
#Kika på varför den dör om den inte hittar några fel

if statDic == {}:
    #st.image('Images/Green.png')
    st.success('All activeties have been completed!', icon="💯")
elif 'Failed' in statDic.values():
    #st.image('Images/Red.png')
    st.error('Some activeties have failed!', icon="🙈")
else:
    st.warning('Some activeties are still running!', icon="🏃")






st.subheader(f'Source Systems that have ran between {start_time} and {end_time}:')

#st.write(filtered_data_time['Source System'].unique())
#occ = filtered_data_time.groupby(['Source System'])

#filtered_data_time

#occ2 = filtered_data_time.groupby(['Source System', 'Load Step Status']).count() #Use size to include NaN values such as Complete etc


#occ3 = filtered_data_time['Source System'].hist(by=filtered_data_time['Load Step Status'])

#bin = df2['Source System'].unique().size
#hist = np.histogram(a=df2, bins= 10 )


#occ4 = df2.groupby(['Source System', 'Load Step Status']).size()
#occ4

#df2


#for sys in df2['Source System'].unique():
#    dbl_flt = df2[df2['Source System'] == sys]
#    statuses = dbl_flt['Load Step Status'].value_counts()
#    st.bar_chart(statuses)





df2 = filtered_data_time_sys[['Source System', 'Load Step Status']].copy()
histDic = {}

for sta in STEP_STATUSES:
    statDic = {}
    for sys in df2['Source System'].unique():
        dbl_flt = df2[df2['Source System'] == sys]
        statuses = dbl_flt['Load Step Status'].value_counts()
        cur_sta = statuses.get(sta)
        if cur_sta != None:
            statDic.update({sys : statuses.get(sta)})
        else:
            statDic.update({sys : 0})
    histDic.update({sta : statDic})
    
#histDic

st.bar_chart(histDic)



actdbRes = pd.DataFrame()
st.subheader('Source Files that have been ran:')
sofidf = filtered_data_time_sys[['Source System', 'Source File', 'Load Step Status']]
#lowcol1, lowcol2 = st.columns(2)

#maybe change it into generating tabs that you can click instead?



for sys in sofidf['Source System'].unique():
    st.subheader(f'Source Files and their statuses that have been ran by {sys}')
    actsysdf = sofidf[sofidf['Source System'] == sys]    
    #with lowcol1:
        #act_flt = st.multiselect('Select Source Files:', options=actsysdf['Source File'].unique(),default=actsysdf['Source File'].unique(),key=f'{sys}-key')


    for sta in STEP_STATUSES:
        actDic = {}
        for act in actsysdf['Source File'].unique():
            act_flt = actsysdf[actsysdf['Source File'] == act]
            statuses = act_flt['Load Step Status'].value_counts()
            cur_sta = statuses.get(sta)
            if cur_sta != None:
                actDic.update({act : statuses.get(sta)})
            else:
                actDic.update({act : 0})
        histDic.update({sta : actDic})
    
    #with lowcol2:
    st.bar_chart(histDic)
    
    




    #actdic = {}
    #st.subheader(f'Activeties and their statuses that have been ran by {sys}')
    #lowcol1, lowcol2 = st.columns(2)
    #dbl_flt = actdf[actdf['Source System'] == sys]
    #with lowcol1:
    #act_flt = st.multiselect('Select activeties:', options=dbl_flt['Load Step'].unique(),default=dbl_flt['Load Step'].unique())
    #for sta in STEP_STATUSES:
    #    for act in dbl_flt['Load Step'].unique():
    #        actdic.update({})
            

        










#st.bar_chart(df2, )
#st.pyplot(occ3)

#filtered_data_time['Source System'].hist(by=filtered_data_time['Source System'])

#bar_data = np.histogram(occ, bins=len(filtered_source_systems))
#st.bar_chart(occ2)


#['Source System'].unique() & df['Run Date'].dt > 

#st.write()

#for sys in filtered_data_time['Source System'].unique():
#    dbl_flt = filtered_data_time[filtered_data_time['Source System'] == sys]
#    #Very confused over how to make the histogram below work properly
#    bar_data = np.histogram(dbl_flt['Run Date'].dt.hour, bins=hours, range=(0, hours))[0]
#    st.subheader(f'{sys} run times')
#    st.bar_chart(bar_data)