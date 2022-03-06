import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from urllib.request import urlopen
import json
import pandas as pd
import numpy as np


df = pd.read_csv('../data analysis code/data/complete.csv',
                 converters={'fips': lambda x: str(x)})

schools = np.append(df.search_school.unique(),'Select all')
industries = np.append(df.current_NAICS_title.unique(),'Select all')

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

print('a')
app = dash.Dash(__name__)

app.layout = html.Div([
        dcc.Dropdown(schools, 
        id='School',
        placeholder='Filter by school',
        searchable = True
        ),
        dcc.Dropdown(industries,
        id='Industry',
        placeholder='Filter by industry',
        searchable = True
        ),
    dcc.Graph(id="choropleth"),
    ])
print('b')
@app.callback(
    Output("choropleth", "figure"), 
    [Input("School", "value"),
    Input("Industry", "value")]
    )

def display_choropleth(school, industry):
    if school == 'Select all' and  industry != 'Select all':
        num = df[(df.current_NAICS_title == industry)].fips.value_counts()
    if industry == 'Select all' and school != 'Select all':
        num = df[(df.search_school == school)].fips.value_counts()
    if industry == 'Select all' and school == 'Select all':
        num = df.fips.value_counts()
    else:
        num = df[(df.current_NAICS_title == industry) &
             (df.search_school == school)].fips.value_counts()

    num = num.reset_index()
    num = num.rename({'index':'fips', 'fips':'counts'}, axis=1)

    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    fig = px.choropleth_mapbox(num, geojson=counties, locations='fips', color='counts',
                           color_continuous_scale='fall',
                           range_color=(0, num[num.fips!='nan'].counts.max()),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.8,
                           labels={'counts':'count'}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
