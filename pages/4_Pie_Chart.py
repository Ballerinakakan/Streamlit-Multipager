import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Home as hm

st.title('A piechart of pick-up hours')

pie_data = np.histogram(hm.data[hm.DATE_COLUMN].dt.hour, bins=24, range=(0, 23))[0]

#st.text(np.array2string(pie_data))
#myLables = ['00', '01', '02', '03', '04','05','06','07','08','09','10','11','12','13', '14', '15', '16', '17','18','19','20','21','22','23']

lables = []
x = range(0, 24)
for n in x:
    lables.append(n)


fig1, ax1 = plt.subplots()
ax1.pie(pie_data, labels=lables, startangle=90, counterclock=False)
ax1.axis('equal')

st.pyplot(fig1)

#lables
#plt.pie(pie_data, labels=lables)
