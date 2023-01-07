import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title=' Forest Coverage data Analysis',
    page_icon='📈',
    layout='wide'
)


Years=['1990','1991','1992','1993','1994','1995','1996','1997','1998','1999',
'2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']

@st.cache
def load_data():
    df=pd.read_csv('..\\data\\forest_coverage_percent.csv')
    df.rename({'geo':'Country'},axis=1,inplace=True)
    df.set_index('Country',inplace=True)
    df.sort_values('Country',inplace=True)
    df['Total']=df[Years].sum(axis=1)
    df['Average']=df.mean(axis=1)
    df['Minimum']=df.min(axis=1)
    df['Maximum']=df.max(axis=1)
    return df

st.title('Forest Coverage Percentage')
df=load_data()
st.dataframe(df,use_container_width=True)

countries= df.index.unique().tolist()
Graphs = ['bar','pie','line','area','funnel']
c1,c2 = st.columns(2)
country = c1.selectbox("Select a Country", countries)
Graph = c2.selectbox("Select a Graph type", Graphs)



st.header('Country wise Visualization')
cdf = df.loc[country,Years].reset_index()
cdf.rename({'index':'Years'},axis=1, inplace=True)
if Graph == Graphs[0]:
    fig = px.bar(cdf, 'Years',country, title=f'{country}  forest coverage percentage')
if Graph == Graphs[1]:
    fig = px.pie(cdf, 'Years',country, title=f'{country}  forest coverage percentage')
if Graph == Graphs[2]:
    fig = px.line(cdf, 'Years',country, title=f'{country}  forest coverage percentage')
if Graph == Graphs[3]:
    fig = px.area(cdf, 'Years',country, title=f'{country}  forest coverage percentage')
if Graph == Graphs[4]:
    fig = px.funnel(cdf, 'Years',country, title=f'{country}  forest coverage percentage')
st.plotly_chart(fig, use_container_width=True)

st.header('Comparison of Country')
clist = st.multiselect("Select countries to compare", countries, default='India')
cdf = df.loc[clist, Years].T # T to rotate the data in 90deg
cdf.rename({'index':'Years'},axis=1,inplace=True)
st.write(cdf)
figc = px.line(cdf,cdf.index, clist, title=f'Comparing {", ".join(clist)}')

st.plotly_chart(figc, use_container_width=True)


df.sort_values(by='Total', ascending=False, inplace=True)
fig1=px.bar(df, x=df.index, y='Total',title='Total forest coverage percent')
st.plotly_chart(fig1,use_container_width=True)

dfavg = df.sort_values(by='Average').reset_index()
dfavg.rename({'index':'Country'},axis=1,inplace=True)
fig2=px.bar(dfavg, 'Country', 'Average', title="Average percent of forest coverage by Country")
st.plotly_chart(fig2,use_container_width=True)

dfmin=df.sort_values(by='Minimum').reset_index()
dfmin.rename({'index':'Country'},axis=1,inplace=True)
fig3=px.bar(dfmin,'Country','Minimum',title='Minimum forest coverage by the Country' )
st.plotly_chart(fig3,use_container_width=True)

dfmax=df.sort_values(by='Maximum').reset_index()
dfmax.rename({'index':'Country'},axis=1,inplace=True)
fig4=px.bar(dfmax,'Country','Maximum',title='Maximum forest coverage by the Country' )
st.plotly_chart(fig4,use_container_width=True)

dfcomp=df.sort_values(by='Country',ascending=False,inplace=True)
fig5 = px.line(df, x=df.index, y='Maximum',title='Maximum and Minimum forest coverage by Country comparison')
fig5.add_scatter(x=df.index, y=df['Minimum'], mode='lines',)
st.plotly_chart(fig5,use_container_width=True)






































