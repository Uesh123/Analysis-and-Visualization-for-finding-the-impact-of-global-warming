import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title='Carbon dioxide data Analysis',
    page_icon='📈',
    layout='wide'
)

years=['1895','1896','1897','1898','1899','1900','1901','1902','1903','1904','1905','1906','1907','1908','1909',
'1910','1911','1912','1913','1914','1915','1916','1917','1918','1919','1920','1921','1922','1923','1924',
'1925','1926','1927','1928','1929','1930','1931','1932','1933','1934','1935','1936','1937','1938','1939',
'1940','1941','1942','1943','1944','1945','1946','1947','1948','1949','1950','1951','1952','1953','1954',
'1955','1956','1957','1958','1959','1960','1961','1962','1963','1964','1965','1966','1967','1968','1969',
'1970','1971','1972','1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983','1984',
'1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999',
'2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014']


@st.cache
def load_data():
    df=pd.read_csv('data\\co2_emissions_tonnes_per_person.csv')
    df.rename({'geo':'Country'},axis=1,inplace=True)
    df.set_index('Country',inplace=True)
    df.drop(['1800','1801','1802', '1803', '1804', '1805', '1806', '1807', '1808', '1809', '1810', '1811', '1812', '1813',
    '1814','1815', '1816', '1817', '1818', '1819', '1820', '1821', '1822', '1823', '1824', '1825', '1826', '1827', '1828',
    '1829', '1830', '1831','1832', '1833', '1834','1835','1836', '1837', '1838', '1839', '1840', '1841', '1842', '1843',
    '1844', '1845', '1846', '1847', '1848', '1849', '1850', '1851', '1852', '1853', '1854', '1855', '1856', '1857', '1858', '1859', '1860', '1861', '1862',
    '1863', '1864', '1865', '1866', '1867','1868', '1869', '1870','1871', '1872', '1873', '1874','1875', '1876', '1877', '1878', '1879', '1880', '1881',
    '1882','1883', '1884', '1885', '1886', '1887','1888', '1889','1890', '1891','1892', '1893', '1894'], axis=1,inplace=True)
    df['Total']=df[years].sum(axis=1)
    df['Average']=df.mean(axis=1)
    df['Maximum']=df.max(axis=1)
    df.sort_index(inplace=True)
    return df
st.title('CO2 Emissions Tonnes Per Person')
df=load_data()
st.dataframe(df,use_container_width=True)

countries= df.index.unique().tolist()
Graphs = ['bar','pie','line','area','funnel']
c1,c2 = st.columns(2)
country = c1.selectbox("Select a Country", countries)
Graph = c2.selectbox("Select a Graph type", Graphs)



st.header('Country wise Visualization')
cdf = df.loc[country,years].reset_index()
cdf.rename({'index':'Years'},axis=1, inplace=True)
if Graph == Graphs[0]:
    fig = px.bar(cdf, 'Years',country, title=f'{country} co2 emissions tonnes by per person')
if Graph == Graphs[1]:
    fig = px.pie(cdf, 'Years',country, title=f'{country} co2 emissions tonnes by per person')
if Graph == Graphs[2]:
    fig = px.line(cdf, 'Years',country, title=f'{country} co2 emissions tonnes by per person')
if Graph == Graphs[3]:
    fig = px.area(cdf, 'Years',country, title=f'{country} co2 emissions tonnes by per person')
if Graph == Graphs[4]:
    fig = px.funnel(cdf, 'Years',country, title=f'{country} co2 emissions tonnes by per person')
st.plotly_chart(fig, use_container_width=True)

st.header('Comparison of Country')
clist = st.multiselect("Select countries to compare", countries, default='India')
cdf = df.loc[clist, years].T # T to rotate the data in 90deg
cdf.rename({'index':'Years'},axis=1,inplace=True)
st.write(cdf)
figc = px.line(cdf,cdf.index, clist, title=f'Comparing {", ".join(clist)}')

st.plotly_chart(figc, use_container_width=True)

df.sort_values(by='Total', ascending=False, inplace=True)
fig1=px.bar(df, x=df.index, y='Total',title='Total co2 emissions tonnes per person')
st.plotly_chart(fig1, use_container_width=True)

dfavg = df.sort_values(by='Average').reset_index()
dfavg.rename({'index':'Country'},axis=1,inplace=True)
fig2=px.bar(dfavg, 'Country', 'Average', title="Avgrage Use of vehicle per 1000 person")
st.plotly_chart(fig2, use_container_width=True)

dfmax=df.sort_values(by='Maximum').reset_index()
dfmax.rename({'index':'Country'},axis=1,inplace=True)
fig3=px.bar(dfmax,'Country','Maximum',title='Maximum co2 emission tonnes per person by Country' )
st.plotly_chart(fig3, use_container_width=True)