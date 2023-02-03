import streamlit as st
import pandas as pd
import numpy as np
import time as tm
import datetime as dt
import dateutil.parser as dp
import Home as hm
import streamlit_timeline as st_tl


basedf = hm.data2
basedf['Run Date'] = pd.to_datetime(basedf['Run Date'])
#curTime = dt.datetime.now()
curTime = dt.datetime(2022, 3, 15, 1, 0, 0)

option = st.selectbox('Time frame:', ('14 days', '30 days', '90 days'))

if(option == '14 days'):
    startTime = curTime - dt.timedelta(days=14)
elif (option == '30 days'):
    startTime = curTime - dt.timedelta(days=30)
else:
    startTime = curTime - dt.timedelta(days=90)

timeFiltdf = basedf[ (basedf['Run Date'] >= startTime) & (basedf['Run Date'] <= curTime)]

selected_source_file = st.selectbox('Select source File:', \
    options= timeFiltdf['Sourcefile'].unique())


selFildf = timeFiltdf[timeFiltdf['Sourcefile'] == selected_source_file]

selFildf

reduceddf = selFildf[['Sourcefile Name', 'Sourcefile Size', 'Run Date']].copy()
reduceddf

skibidi = reduceddf.groupby(['Sourcefile Name', 'Run Date'])
skibidi

#shabooki = reduceddf.aggregate(['Sourcefile Name', 'Run Date'])
#shabooki

#for( reduceddf['Sourcefile Name'].groupby()):
 #   wowhelpme = reduceddf.pivot_table()



#nonCompFiltDF = timeFiltdf[ timeFiltdf['']]
