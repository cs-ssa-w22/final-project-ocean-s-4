# Import required libraries
import plotly.express as px
from urllib.request import urlopen
import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go



# Multi-dropdown options

app = dash.Dash(__name__)
server = app.server


# Load data
df = pd.read_csv('complete.csv',
                 converters={'fips': lambda x: str(x)})

schools = np.append(df.search_school.unique(),'Select all')
industries = np.append(df.current_NAICS_title.unique(),'Select all')

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
    

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            'Career Outlook',

                        ),
                        html.H4(
                            'know your alumni',
                        )
                    ],

                    className='eight columns'
                ),
            ],
            id="header",
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                       
                        html.P(
                            'Filter by school:',
                            className="control_label"
                        ),
                        dcc.Dropdown(schools, 
                        id='School',
                        placeholder='Filter by school',
                        searchable = True
                        ),
                        html.P(
                            'Filter by industry:',
                            className="control_label"
                        ),
                        dcc.Dropdown(industries,
                        id='Industry',
                        placeholder='Filter by industry',
                        searchable = True
                        ),
                        html.Br(), 
                        html.P(
                            [html.Strong ('Data Source:') ,html.Br(),
                            html.Li(['Alumni profile data:', html.Br(),
                            'LinkedIn: ', 
                             html.A("https://www.linkedin.com", href="https://www.linkedin.com"),
                             html.Br()]),
                            html.Li(['Salary data: ', html.Br(),
                             'Bureau of Labor Statistics: ',
                             html.A("https://www.bls.gov/oes/", href="https://www.bls.gov/oes/"),
                             html.Br()]),
                            html.Li(['Industry code data:', html.Br(),
                            'Business Source Complete|EBSCO: ',
                             html.A("https://www.ebsco.com", href="https://www.ebsco.com")])]
                        )
                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='pie_graph1')
                            ],
                            id="countGraphContainer",
                            className="pretty_container"
                        )
                    ],
                    id="rightCol",
                    className="ten columns"
                )
            ],
            className="row"
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id="choropleth")
                    ],
                    className='pretty_container fourteen columns',
                ),
#                 html.Div(
#                     [
#                         dcc.Graph(id='individual_graph')
#                     ],
#                     className='pretty_container four columns',
#                 ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='bar_graph')
                    ],
                    className='pretty_container six columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='sankey_graph')
                    ],
                    className='pretty_container seven columns',
                ),
            ],
            className='row'
        ),
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)



# Create callbacks

############################## pie plot ############################## 
@app.callback(
    Output("pie_graph1", "figure"), 
    [Input("School", "value"),
    Input("Industry", "value")]
    )

def plot_pie(set_school,set_industry):
    '''
    Draw pie plot for major distribution part.
    '''
    data = df[['search_school', 'current_NAICS', 'current_NAICS_title','current_avg_salary','major']]
    data['major'] = data['major'].replace(['Business Administration, Management and Operations'],\
                                          'Business Administration<br> and Management and Operations')
    data['major'] = data['major'].replace(['Business Administration and Management, General'],\
                                          'Business Administration<br> and Management, General ')
    data['major'] = data['major'].replace(['Business, Management, Marketing, and Related Support Services'],\
                                          'Business, Management, Marketing<br>and Related Support Services')
    data['major'] = data['major'].replace(['Logistics, Materials, and Supply Chain Management'],\
                                          'Logistics, Materials<br>and Supply Chain Management')
    data = data.dropna()
    # get input
    if set_school == 'Select all' and  set_industry != 'Select all':
        data = data[data['current_NAICS_title'] == set_industry]
        major_data = data.groupby(['major']).count()
        major_data = major_data[(major_data['search_school'] >= 3)]
        major_data.reset_index(inplace=True)
#         fig = px.pie(major_data, values='search_school', names='major',\
#                      color_discrete_sequence = px.colors.diverging.Fall, height= 500)
    elif set_industry == 'Select all' and set_school != 'Select all':
        data = data[data['search_school'] == set_school]
        major_data = data.groupby(['major']).count()
        major_data = major_data[(major_data['search_school'] >= 3)]
        major_data.reset_index(inplace=True)
#         fig = px.pie(major_data, values='search_school', names='major',\
#                      color_discrete_sequence = px.colors.diverging.Fall, height= 500)

    elif set_industry == 'Select all' and set_school == 'Select all':
        data = data
        major_data = data.groupby(['major']).count()
        major_data = major_data[(major_data['search_school'] >= 10)]
        major_data.reset_index(inplace=True)

    else:
        data = data[(data['current_NAICS_title'] == set_industry) & \
                    (data['search_school'] == set_school)]
        major_data = data.groupby(['major']).count()
        major_data = major_data[(major_data['search_school'] >= 3)]
        major_data.reset_index(inplace=True)
#         fig = px.pie(major_data, values='search_school', names='major',\
#                      color_discrete_sequence = px.colors.diverging.Fall, height= 500)
    fig = px.pie(major_data, values='search_school', names='major',\
                 color_discrete_sequence = px.colors.diverging.Fall)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig
############################## bar plot ############################## 

@app.callback(
    Output(component_id='bar_graph', component_property='figure'),
    [Input("School", "value")]
)

def plot_bar(set_school):
    '''
    Draw bar plot for industry distribution part.
    '''
    data = df[['search_school', 'current_NAICS', 'current_NAICS_title','current_avg_salary']]
    data = data.dropna()
    # get input
    if set_school == 'Select all':
        data = data
    else:
        data = data[data['search_school'] == set_school]
   
    ## plot
    data['number'] = data.groupby(['current_NAICS'])['current_avg_salary'].transform('count')
    data = data.drop_duplicates(subset=['current_NAICS_title'], keep="last")
    fig = px.bar(data, x='current_NAICS', y='number',
                 hover_data=['current_avg_salary','current_NAICS_title'], color='number',
                 color_continuous_scale='fall',
                 labels={'current_NAICS': 'Industry Code', 'number':'Number of Alumni'}, height=600)
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig.update(layout_coloraxis_showscale=False)


    return fig

############################## sankey plot ############################## 
@app.callback(
    Output(component_id='sankey_graph', component_property='figure'),
    [Input("School", "value"),
    Input("Industry", "value")]
)
def go_sankey(set_school, set_industry):
    '''
    Draw sankey diagram for industry flow part.
    '''
    # get necessary columns
    # get necessary columns
    raw_data = df[['search_school', 'previous_NAICS_title', 'current_NAICS_title']]
    data = raw_data.dropna()
    # get input
    if set_school == 'Select all' and  set_industry != 'Select all':
        data = data[data['previous_NAICS_title'] == set_industry]
    elif set_industry == 'Select all' and set_school != 'Select all':
        data = data[data['search_school'] == set_school]
    elif set_industry == 'Select all' and set_school == 'Select all':
        data = data
    else:
        data = data[(data['previous_NAICS_title'] == set_industry) & \
                    (data['search_school'] == set_school)]

    # only get different values  
    data = data[data['previous_NAICS_title'] != data['current_NAICS_title']]
    # only keep previous and current naics title
    data = data[['previous_NAICS_title', 'current_NAICS_title']]
    
    # get nodes, source and target
    all_nodes = data['previous_NAICS_title'].tolist() + data['current_NAICS_title'].tolist()
    source_indices = [all_nodes.index(previous_NAICS_title) for previous_NAICS_title in data['previous_NAICS_title']]
    target_indices = [all_nodes.index(current_NAICS_title, len(data['previous_NAICS_title'])) for current_NAICS_title in data['current_NAICS_title']]
    
    # create all source and target combinations
    comb = []
    for i in range(len(source_indices)):
        source, target = (source_indices[i], target_indices[i])
        comb.append((source, target))
    # count occur
    map_counts = {}
    for tup in comb:
        if tup not in map_counts:
            map_counts[tup] = 1
        else:
            map_counts[tup] += 1
    # create values
    values = []
    for tup in comb:
        values.append(map_counts[tup])
    
    # set colors
    colors = px.colors.diverging.Fall
    node_colors_mappings = dict([(node, np.random.choice(colors)) for node in all_nodes])
    node_colors = [node_colors_mappings[node] for node in all_nodes]
    edge_colors = [node_colors_mappings[node] for node in data['current_NAICS_title']]
    
    fig = go.Figure(data=[go.Sankey(node = dict(pad = 35, thickness = 10, line = dict(color = "black", width = 1.0),
                    label =  all_nodes, color =  node_colors),
                    link = dict(source =  source_indices, target =  target_indices, value =  values, color = edge_colors))])
    
    fig.update_layout(title_text="Industry Flow", height=600, font=dict(size = 10, color = 'black'))
    return fig


############################## map plot ############################## 

@app.callback(
    Output("choropleth", "figure"), 
    [Input("School", "value"),
    Input("Industry", "value")]
    )

def display_choropleth(school, industry):
    '''
    Draw the map.
    '''

    if school == 'Select all' and  industry != 'Select all':
        num = df[df.current_NAICS_title == industry][['fips','location']].value_counts()
    elif industry == 'Select all' and school != 'Select all':
        num = df[df.search_school == school][['fips','location']].value_counts()
    elif industry == 'Select all' and school == 'Select all':
        num = df[['fips','location']].value_counts()
    else:
        num = df[(df.current_NAICS_title == industry) &
             (df.search_school == school)][['fips','location']].value_counts()

    num = num.reset_index()
    num = num.rename({'index':'fips', 0:'counts'}, axis=1)

    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    fig = px.choropleth_mapbox(num, geojson=counties, locations='fips', color='counts',
                           color_continuous_scale='fall', hover_name='location',
                           hover_data={'fips':False},
                           range_color=(0, num.counts.max()),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.8,
                           labels={'counts':'Number of Alumni', 'location':'location'}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig


# Main
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
