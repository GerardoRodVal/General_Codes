import plotly.express as px
import numpy as np
import pandas as pd

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
df = pd.read_csv(url, delimiter=',', header='infer')

df_interest = df.loc[
    df['Country/Region'].isin(['United Kingdom', 'US', 'Italy', 'Brazil', 'India'])
    & df['Province/State'].isna()]

df1 = df_interest.transpose()
df1 = df1.drop(['Province/State', 'Country/Region', 'Lat', 'Long'])
df1 = df1.loc[(df1 != 0).any(1)]
df1.index = pd.to_datetime(df1.index)
df1 = df1.diff() #day on day changes

fig = px.line(x=df1.index, y= df1[df1.columns[0]],title = 'Daily Deaths due to COVID-19')
fig.show()
