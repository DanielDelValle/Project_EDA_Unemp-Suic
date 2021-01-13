import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
import psutil
import plotly.io as pio


def intersector(df1, df2, col1, col2):
    """Returns 2 dataframes reduced to common values according specified columns.
        Col1 & Col2 must be string"""

    df1list = set(df1[col1].unique())
    df2list = set(df2[col2].unique())
    countrylist = list(set(df1list).intersection(df2list))

    df1 = df1.loc[df1[col1].isin(countrylist)]
    df2 = df2.loc[df2[col2].isin(countrylist)]

    return df1, df2

suicide = pd.read_csv("C:\\DATA_SCIENCE\\PROYECTO\\documentation\\who_suicide_statistics.csv")
unemployment = pd.read_csv("C:\\DATA_SCIENCE\\PROYECTO\\documentation\\unemployment_all_ratio.csv")

suic, unemp = intersector(df1=suicide, df2=unemployment, col1="country", col2="Country")


suic = suic.rename(columns={'sex': 'gender'})

suic = suic[suic['year'] >= 2000]                                              

suic['age'] = suic['age'].str.rstrip('years ')                                  

suic["suic_100k"] = ((suic.suicides_no/suic.population)*100000).round(2)

aggregation_functions = {'suic_100k': 'mean'}

suic_ages_mean = suic.groupby(suic['age']).aggregate(aggregation_functions).sort_values("suic_100k",ascending=False).round(2)

suic_countries_mean = suic.groupby('country').aggregate(aggregation_functions).sort_values("suic_100k",ascending=True).round(2)

most_per_100k = suic.groupby("country").sum().sort_values("suic_100k", ascending=False).round(2).head()
least_per_100k = suic.groupby("country").sum().sort_values("suic_100k", ascending=False).round(2).tail()

most_of_all = suic.groupby("country").sum().sort_values("suicides_no", ascending=False).head()
least_of_all = suic.groupby("country").sum().sort_values("suicides_no", ascending=False).tail()

suic_pivot = pd.pivot_table(suic, index = ['country', 'year'], values = ['suicides_no', 'suic_100k']).round(2)

sp_su = suic_pivot.loc["Spain"]
lt_su = suic_pivot.loc["Lithuania"]
ru_su = suic_pivot.loc["Russian Federation"]
tu_su = suic_pivot.loc["Turkey"]
sa_su = suic_pivot.loc["South Africa"]
suic_age_group = suic.groupby(['gender']).mean().round(2)