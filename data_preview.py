import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import missingno as msno
from sqlalchemy import create_engine
import pymysql

#config StreamLit
st.set_page_config(layout='wide')

#setting up data
data = {}

table_list = [
    'daily_market_cap',
    'daily_price',
    'daily_vol',
    'hourly_market_cap',
    'hourly_price',
    'hourly_vol',
    'minute_market_cap',
    'minute_price',
    'minute_vol',
    'temp_market_cap',
    'temp_price',
    'temp_vol'
]


#def to print general information about the data
def data_size(data):
    st.text("{:<30} {:<30} {:<30}".format("Table Name", "Number of Periods", "Number of Coins"))
    for table_name in data.keys():
        m,n = data[table_name].shape
        st.text("{:<30} {:<30} {:<30}".format(table_name, m, n))



#programme beggins here
#st.title("<h1 style='text-align: center; '>Coins Database Preview</h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: black;'>Coins Database Preview</h1>", unsafe_allow_html=True)


placeholder = st.empty()

# Replace the placeholder with some text:
placeholder.text("Loading data..")

#loading data
for table_name in table_list:
    engine=create_engine('mysql+pymysql://root:123456@35.185.176.202/crypto')
    data[table_name] = pd.read_sql_table(table_name, engine)

placeholder.text("Data loaded..")
time.sleep(2)
placeholder.empty()

st.write("Tables count: {}".format(len(data.keys())))

#print general info
data_size(data)



for table_name in table_list:
    df1 = data[table_name]
    df2 = df1.isnull()
    df3 = df2.melt(value_name="Missing")
    m,n = df1.shape 
    total_nValues = m * n;

#st.write(df1.head())

    st.subheader('Chart Analysis of {}: {:.2f}% missing data'.format(table_name, df2.sum().sum()/total_nValues * 100))

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        #sns.color_palette("viridis", as_cmap=True)
        #plt.figure(figsize=(10,15))
        ax = sns.heatmap(df2, cbar=True, xticklabels=['IDs'], cmap="Blues")
        st.pyplot(fig)
        #plt.savefig("hung001.png")

    with col2:
        #fig, ax = plt.subplots()
        #plt.figure(figsize=(10,10))
        ax = sns.displot(data=df3, y="variable", hue="Missing", multiple="fill", aspect=1.25)
        ax.set(yticklabels=[])
        #ax =msno.matrix(df1)
        #st.pyplot(fig)
        st.pyplot(ax.figure)
        #/st.pyplot(plt.show())
        #plt.show()
        #plt.savefig("hung002.png")

# p =msno.matrix(df1)
# st.pyplot(p.figure)
# fig_copy = p.get_figure()
# fig_copy.savefig('Hung003.png', bbox_inches = 'tight')

#msno.matrix(df1)


# fig, ax = plt.subplots()
# ax = sns.displot(
#     data=df1.isna().melt(value_name="missing"),
#     y="variable",
#     hue="missing",
#     multiple="fill",
#     aspect=1.25
# )
# st.pyplot(ax.figure)
# plt.savefig("Hung004.png", dpi=100)


# # Loading the dataset
# df = pd.read_csv("kamyr-digester.csv")
  
# Visualize missing values as a matrix
#p = msno.matrix(df1, figsize=(,70))
#p =msno.matrix(df1)
#st.pyplot(p.figure)
#fig_copy = p.get_figure()
#fig_copy.savefig('Hung006.png', bbox_inches = 'tight')