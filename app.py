import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import utils.dash_reuable_components as drc
from utils.read_datasets import read_sklearn_datasets, read_csv_datasets
from utils import figures

app = dash.Dash(__name__)
server = app.server
read_datasets = read_sklearn_datasets

app.layout = html.Div(children=[
    html.Div(className="banner", children=[
        html.Div(className='container scalable', children=[
            html.H2(html.A(
                'EDA',
                href='',
                style={
                    'text-decoration': 'none',
                    'color': 'inherit',
                }
            )),

            html.A(
                html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png"),
                href='https://plot.ly/products/dash/'
            )
        ]),
    ]),

    html.Div(id='body', className='container scalable', children=[
        html.Div(className='row', children=[
            html.Div(
                id='div-graphs',
                children=dcc.Graph(
                    id='graph',
                    style={'display': 'none'}
                )
            ),

            html.Div(
                className='three columns',
                style={
                    'min-width': '24.5%',
                    'max-height': 'calc(100vh - 85px)',
                    'overflow-y': 'auto',
                    'overflow-x': 'hidden',
                },
                children=[
                    drc.Card([
                        drc.NamedDropdown(
                            name='Select Data Source',
                            id='dropdown-select-data-source',
                            options=[
                                {'label': 'Sklearn', 'value': 'sklearn'},
                                {'label': 'CSV', 'value': 'csv'},
                            ],
                            clearable=False,
                            searchable=False,
                            value='sklearn'
                        ),
                        drc.NamedDropdown(
                            name='Select Dataset',
                            id='dropdown-select-dataset',
                            clearable=False,
                            searchable=False,
                        ),
                    ]),
                    drc.Card([
                        drc.NamedDropdown(
                            name='Select Graph',
                            id='dropdown-select-graph',
                            options=[
                                {'label': 'Scatter', 'value': 'scatter'},
                                {'label': 'Table', 'value': 'table'},
                                {'label': 'Distribution', 'value': 'distribution'}
                            ],
                            clearable=False,
                            searchable=False,
                            value='scatter'
                        ),
                        drc.NamedDropdown(
                            name='X-axis',
                            id='graph-x-axis',
                            clearable=False,
                            searchable=False,
                            value=''
                        ),
                        drc.NamedDropdown(
                            name='Y-axis',
                            id='graph-y-axis',
                            clearable=False,
                            searchable=False,
                            value=''
                        )
                    ])
                ]
            )
        ])
    ])
])

# Setting component
@app.callback(
    Output('dropdown-select-dataset', 'options'),
    [Input('dropdown-select-data-source', 'value')]
)
def change_datasource(data_source):
    global read_datasets
    if data_source == 'sklearn':
        read_datasets = read_sklearn_datasets
        dataset_names=[
            {'label': 'Iris', 'value': 'iris'},
            {'label': 'Boston House-Prices', 'value': 'boston house-prices'},
        ]
    elif data_source == 'csv':
        read_datasets = read_csv_datasets
        dataset_names=[
            {'label': 'Titanic_train', 'value': 'titanic_train'},
            {'label': 'Titanic_test', 'value': 'titanic_test'},
        ]
    
    return dataset_names

# Setting component
@app.callback(
    Output('dropdown-select-dataset', 'value'),
    [Input('dropdown-select-data-source', 'value')]
)
def change_datasource(data_source):
    global read_datasets
    if data_source == 'sklearn':
        return 'iris'
    elif data_source == 'csv':
        return 'titanic_train'

@app.callback(
    Output('graph-x-axis', 'options'),
    [Input('dropdown-select-dataset', 'value')]
)
def update_dropdown_xaix(ds_name):
    global read_datasets
    ds_df = read_datasets(ds_name)
    label = [{'label': i, 'value': i} for i in ds_df.columns]
    return [{'label': i, 'value': i} for i in ds_df.columns]

@app.callback(
    Output('graph-y-axis', 'options'),
    [Input('dropdown-select-dataset', 'value')]
)
def update_dropdown_yaix(ds_name):
    global read_datasets
    ds_df = read_datasets(ds_name)
    label = [{'label': i, 'value': i} for i in ds_df.columns]
    return [{'label': i, 'value': i} for i in ds_df.columns]

@app.callback(
    Output('graph-x-axis', 'disabled'),
    [Input('dropdown-select-graph', 'value')]
)
def disable_dropdown_xaix(graph_name):
    if graph_name == 'table':
        return True
    else:
        return False
        
@app.callback(
    Output('graph-y-axis', 'disabled'),
    [Input('dropdown-select-graph', 'value')]
)
def disable_dropdown_yaix(graph_name):
    if graph_name == 'scatter':
        return False
    else:
        return True

@app.callback(
    Output('graph-x-axis', 'value'),
    [Input('dropdown-select-data-source', 'value'),
    Input('dropdown-select-dataset', 'value'),
    Input('dropdown-select-graph', 'value')]
)
def reset_dropdown_xaix(data_source,
                        dataset,
                        graph_name):
    return ''

@app.callback(
    Output('graph-y-axis', 'value'),
    [Input('dropdown-select-data-source', 'value'),
    Input('dropdown-select-dataset', 'value'),
    Input('dropdown-select-graph', 'value')]
)
def reset_dropdown_yaix(data_source,
                        dataset,
                        graph_name):
    return ''

# Plot
@app.callback(Output('div-graphs', 'children'),
            [Input('dropdown-select-dataset', 'value'),
            Input('dropdown-select-graph', 'value'),
            Input('graph-x-axis', 'value'),
            Input('graph-y-axis', 'value'),])
def update_graph(ds_name,
                graph_type,
                x_axis,
                y_axis):
    
    global read_datasets
    ds_df = read_datasets(ds_name)

    if graph_type == 'scatter':
        if len(x_axis) == 0 or len(y_axis) == 0:
            return None
        else:
            figure = figures.serve_scatter_plot(ds_df[x_axis], ds_df[y_axis], x_axis, y_axis)
    elif graph_type == 'table':
        figure = figures.serve_table_data(ds_df)

    elif graph_type == 'distribution':
        if len(x_axis) == 0:
            return None
        else:
            figure = figures.serve_dist_plot(ds_df[x_axis], x_axis)

    return [
        html.Div(
            className='six columns',
            style={
                'min-width': '24.5%',
                'margin-top': '5px',
                # Remove possibility to select the text for better UX
                'user-select': 'none',
                '-moz-user-select': 'none',
                '-webkit-user-select': 'none',
                '-ms-user-select': 'none'
            },
            children=[
                dcc.Graph(
                    id='graph',
                    figure=figure,
                    style={'height': 'calc(100vh - 90px)'}
                )
            ])
    ]

# Style sheet
external_css = [
    # Normalize the CSS
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
    # Fonts
    "https://fonts.googleapis.com/css?family=Open+Sans|Roboto",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
]

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
     app.run_server(debug=True)