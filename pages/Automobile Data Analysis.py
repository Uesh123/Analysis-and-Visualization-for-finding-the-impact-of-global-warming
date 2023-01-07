import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_icon='📈',
    page_title="Automobile Data Analysis",
    layout='wide'
)

years = ['2002','2003','2004','2005','2006','2007']

@st.cache
def load_data():
    df=pd.read_csv('..\\data\\cars_trucks_and_buses_per_1000_persons.csv')
    df.rename(columns={'geo':'Country'},inplace=True)
    df.set_index('Country',inplace=True)
    df['Total'] = df[years].sum(axis=1)
    df['Avgrage']=df.mean(axis=1)
    df['Maximum']=df.max(axis=1)
    df.sort_index(inplace=True)
    return df

st.title('Cars Trucks and Buses Per 1000 Persons')
df = load_data()
st.dataframe(df,use_container_width=True)

countries= df.index.unique().tolist()
Graphs = ['bar','pie','line','area','histogram']
c1,c2 = st.columns(2)
country = c1.selectbox("Select a Country", countries)
Graph = c2.selectbox("Select a Graph type", Graphs)

st.header("Country wise visualization")
cdf = df.loc[country,years].reset_index()
cdf.rename({'index':'Years'},axis=1, inplace=True)
if Graph == Graphs[0]:
    fig = px.bar(cdf, 'Years',country, title=f'{country} Cars trucks and buses per 1000 persons')
if Graph == Graphs[1]:
    fig = px.pie(cdf, 'Years',country, title=f'{country} Cars trucks and buses per 1000 persons')
if Graph == Graphs[2]:
    fig = px.line(cdf, 'Years',country, title=f'{country} Cars trucks and buses per 1000 persons')
if Graph == Graphs[3]:
    fig = px.area(cdf, 'Years',country, title=f'{country} Cars trucks and buses per 1000 persons')
if Graph == Graphs[4]:
    fig = px.histogram(cdf, 'Years',country, title=f'{country} Cars trucks and buses per 1000 persons')
st.plotly_chart(fig, use_container_width=True)

st.header("Comparison of Countries")
clist = st.multiselect("Select countries to compare", countries, default='India')
cdf = df.loc[clist, years].T # T to rotate the data in 90deg
st.write(cdf)
figc = px.line(cdf,cdf.index, clist, title=f'Comparing {", ".join(clist)}')

st.plotly_chart(figc, use_container_width=True)

df.sort_values(by='Total', ascending=False, inplace=True)
fig1=px.bar(df, x=df.index, y='Total',title='Total number of cars, trucks and buese per 1000 person')
st.plotly_chart(fig1, use_container_width=True)

dfavg = df.sort_values(by='Avgrage').reset_index()
dfavg.rename({'index':'Country'},axis=1,inplace=True)
fig2=px.bar(dfavg, 'Country', 'Avgrage', title="Avgrage Use of vehicle per 1000 person")
st.plotly_chart(fig2, use_container_width=True)

dfmax=df.sort_values(by='Maximum').reset_index()
dfmax.rename({'index':'Country'},axis=1,inplace=True)
fig3=px.bar(dfmax,'Country','Maximum',title='Maximum cars, bus and truck per 1000 person')
st.plotly_chart(fig3, use_container_width=True)