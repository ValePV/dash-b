import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_daq as daq
import dash_cytoscape as cyto
import pandas as pd
import plotly.graph_objs as go

from dash.dependencies import Input, Output, State

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'cb5392c35661370d95f300086accea51/raw/'
    '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
    'indicators.csv')
df1 = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

df2 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

available_indicators = df['Indicator Name'].unique()

markdown_text = '''
### Lorem Ipsum

Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered
'''

nodes = [
    {
        'data':{'id': short, 'label': label},
        'position':{'x': 20*lat, 'y': -20*long}
    }
    for short, label, long, lat in (
        ('la', 'Los Angeles', 34.03, -118.25),
        ('nyc', 'New York', 40.71, -74),
        ('to', 'Toronto', 43.65, -79.38),
        ('mtl', 'Montreal', 45.50, -73.57),
        ('van', 'Vancouver', 49.28, -123.12),
        ('chi', 'Chicago', 41.88, -87.63),
        ('bos', 'Boston', 42.36, -71.06),
        ('hou', 'Houston', 29.76, -95.37)
    )
]

edges = [
    {'data': {'source':source, 'target':target}}
    for source, target in (
        ('van', 'la'),
        ('la', 'chi'),
        ('hou', 'chi'),
        ('to', 'mtl'),
        ('mtl', 'bos'),
        ('nyc', 'bos'),
        ('to', 'hou'),
        ('to', 'nyc'),
        ('la', 'nyc'),
        ('nyc', 'bos')
    )
]

elements = nodes + edges

app.layout = html.Div([
    html.Div([
        html.H1(children='BUPRY',
        style = {
            'textAlign':'center',
            'textTransform' : 'uppercase',
            'margin':'15px 0'
        })
    ]),
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Page One', children=[
            html.Div([
                html.Div([

                    html.Div([
                        dcc.Dropdown(
                            id='crossfilter-xaxis-column',
                            options=[{'label': i, 'value': i} for i in available_indicators],
                            value='Fertility rate, total (births per woman)'
                        ),
                        dcc.RadioItems(
                            id='crossfilter-xaxis-type',
                            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                            value='Linear',
                            labelStyle={'display': 'inline-block', 'marginTop':'15px'}
                        )
                    ],
                    style={'width': '50%', 'display': 'inline-block', 'padding':'10px'}),

                    html.Div([
                        dcc.Dropdown(
                            id='crossfilter-yaxis-column',
                            options=[{'label': i, 'value': i} for i in available_indicators],
                            value='Life expectancy at birth, total (years)'
                        ),
                        dcc.RadioItems(
                            id='crossfilter-yaxis-type',
                            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                            value='Linear',
                            labelStyle={'display': 'inline-block', 'marginTop':'15px'}
                        )
                    ], style={'width': '49%', 'float': 'right', 'display': 'inline-block', 'padding':'10px'})
                ], style={
                    'borderBottom': 'thin lightgrey solid',
                    'backgroundColor': 'rgb(250, 250, 250)',
                    'padding': '10px 5px'
                }),
                
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='crossfilter-indicator-scatter',
                            hoverData={'points': [{'customdata': 'Japan'}]}
                        )
                    ], style={'width': '47%', 'display': 'inline-block', 'padding': '20', 'border':'1px solid #ccc', 'marginRight':'10px'}),
                    html.Div([
                        html.Div([
                            dcc.Graph(id='x-time-series')
                        ], style={'padding':'10px', 'border':'1px solid #ccc', 'marginBottom':'20px'}),
                        html.Div([
                            dcc.Graph(id='y-time-series')
                        ], style={'padding':'10px', 'border':'1px solid #ccc'})
                    ], style={'display': 'inline-block', 'width': '47%'}),

                    html.Div(dcc.Slider(
                        id='crossfilter-year--slider',
                        min=df['Year'].min(),
                        max=df['Year'].max(),
                        value=df['Year'].max(),
                        step= 5,
                        marks={str(year): str(year) for year in df['Year'].unique()}
                    ), style={'width': '47%', 'padding':'20px'})
                ], className='row', style={'padding':'15px', 'marginLeft':'0'})

                
            ])
        ]),
        dcc.Tab(label='Page Two', children=[
            html.Div([
                dcc.Markdown(children=markdown_text)
            ], style={'padding':'15px', 'marginTop':'10px'}),
            html.Div([
                html.Div([
                    dcc.Graph(
                    figure=go.Figure(
                    data=[
                        go.Bar(
                            x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                            2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                            y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                            350, 430, 474, 526, 488, 537, 500, 439],
                            name='Rest of world',
                            marker=go.bar.Marker(
                                color='rgb(55, 83, 109)'
                            )
                        ),
                        go.Bar(
                            x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                            2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                            y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                            299, 340, 403, 549, 499],
                            name='China',
                            marker=go.bar.Marker(
                                color='rgb(26, 118, 255)'
                            )
                        )
                    ],
                    layout=go.Layout(
                        title='US Export of Plastic Scrap',
                        showlegend=True,
                        legend=go.layout.Legend(
                            x=0,
                            y=1.0
                        ),
                        margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                    )
                ),
                    style={'height': 300},
                    id='my-graph'
                )
                ], className='nine column', style={'padding':'15px', 'marginLeft':'20px'}),

                html.Div([
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in df2.columns],
                        data=df2.to_dict('records'),
                    )

                ], className='four column', style={'padding':'15px'})


            ], className='row'),
            
                
        ]),
        dcc.Tab(label='Page Three', children=[
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='life-exp-vs-gdp',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=df1[df1['continent'] == i]['gdp per capita'],
                                    y=df1[df1['continent'] == i]['life expectancy'],
                                    text=df1[df1['continent'] == i]['country'],
                                    mode='markers',
                                    opacity=0.7,
                                    marker={
                                        'size': 15,
                                        'line': {'width': 0.5, 'color': 'white'}
                                    },
                                    name=i
                                ) for i in df1.continent.unique()
                            ],
                            'layout': go.Layout(
                                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                                yaxis={'title': 'Life Expectancy'},
                                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                                legend={'x': 0, 'y': 1},
                                hovermode='closest'
                            )
                        }
                    )
                ], style={'width':'80%', 'padding':'15px','display':'inline-block', 'border':'1px solid #ccc'}),
                html.Div([
                    daq.Knob(
                        id='my-daq-knob',
                        min=0,
                        value=3,
                        max=20
                    )
                ], style={'padding':'15px', 'width':'20%', 'display':'inline-block', 'verticalAlign':'top'})
            ],style={'marginTop':'15px', 'padding':'15px'})
        ]),

        dcc.Tab(label='Page Four', children=[
            html.Div([
        
                html.Div([
                    dcc.Dropdown(
                        id='dropdown-update-layout',
                        value='grid',
                        clearable=False,
                        options=[
                            {'label':name.capitalize(), 'value':name}
                            for name in ['grid', 'random', 'circle', 'cose', 'concentric']
                        ]
                    ),
                    cyto.Cytoscape(
                        id='cytoscape-update-layout',
                        layout={'name':'grid'},
                        style={'width':'100%', 'height':'450px'},
                        elements=elements
                    )
                ])
            ], style={'width':'95%','padding':'15px', 'marginTop':'30px', 'border':'1px solid #ccc', 'marginLeft':'45px'})
        ])
        
    ])
])

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]

    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)

@app.callback(Output('cytoscape-update-layout', 'layout'),
              [Input('dropdown-update-layout', 'value')])
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }


if __name__ == '__main__':
    app.run_server(debug=True)
