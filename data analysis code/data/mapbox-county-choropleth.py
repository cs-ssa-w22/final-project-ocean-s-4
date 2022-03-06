import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from urllib.request import urlopen
import json
import pandas as pd


df = pd.read_csv('../data/complete.csv',
                 converters={'fips': lambda x: str(x)})

schools = df.search_school.unique()
industries = df.current_NAICS_title.unique()

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)




app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div([
    html.Div([
        dcc.Dropdown(schools, 
        id='School',
        multi=True, placeholder='Filter by school',
        searchable = True
        )
    ], style={'width': '48%', 'display': 'inline-block'}
    ),

    html.Div([
    dcc.Dropdown(industries,
        id='Industry',
        multi=True, placeholder='Filter by industry',
        searchable = True
        )
    ], style={'width': '48%', 'display': 'inline-block'}
    ),
    ]),
    dcc.Graph(id="choropleth"),
    ])


@app.callback(
    Output("choropleth", "figure"), 
    Input("School", "value"),
    Input("Industry", "value")
    )

def display_choropleth(school, industry):

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
