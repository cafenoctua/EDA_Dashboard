import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

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
                            name='Select Dataset',
                            id='dropdown-select-dataset',
                            options=[
                                {'label': 'Iris', 'value': 'iris'},
                                {'label': 'Boston House-Prices', 'value': 'boston house-prices'}
                            ],
                            value='iris',
                            clearable=False,
                            searchable=False,
                        ),
                        drc.NamedDropdown(
                            name='Select Graph',
                            id='graph-select-update',
                           options=[
                                {'label': 1, 'value': 1},
                                {'label': 2, 'value': 2},
                                {'label': 3, 'value': 3}
                            ],
                            value=1,
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
                            value='table'
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
                    ]),
                ]
            )
        ]),
        html.Div(
            id='graph-space',
            children=[
                html.Div(
                    id='div-graphs1',
                    children=dcc.Graph(
                        id='graph1',
                        style={'display': 'none'}
                    )
                ),
                html.Div(
                    id='div-graphs2',
                    children=dcc.Graph(
                        id='graph2',
                        style={'display': 'none'}
                    )
                ),
                html.Div(
                    id='div-graphs3',
                    children=dcc.Graph(
                        id='graph3',
                        style={'display': 'none'}
                    )
                ),
                # dcc.Graph(
                #         id='graph1',
                #         style={'display': 'none'}
                # )
                # html.Div(
                #     id='div-graphs1',
                #     children=dcc.Graph(
                #         id='graph1',
                #         style={'display': 'none'}
                #     )
                # ),
                # html.Div(
                #     id='div-graphs2',
                #     children=dcc.Graph(
                #         id='graph',
                #         style={'display': 'none'}
                #     )
                # ),
            ]
        ),
    ]),
])

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
    [Input('dropdown-select-dataset', 'value'),
    Input('dropdown-select-graph', 'value')]
)
def reset_dropdown_xaix(dataset,
                        graph_name):
    return ''

@app.callback(
    Output('graph-y-axis', 'value'),
    [Input('dropdown-select-dataset', 'value'),
    Input('dropdown-select-graph', 'value')]
)
def reset_dropdown_yaix(dataset,
                        graph_name):
    return ''

# Plot
def update_graph_base(ds_name,
                graph_type,
                x_axis,
                y_axis):
    global read_datasets
    ds_df = read_datasets(ds_name)

    if graph_type == 'scatter':
        if len(x_axis) == 0 or len(y_axis) == 0:
            raise PreventUpdate
        else:
            figure = figures.serve_scatter_plot(ds_df[x_axis], ds_df[y_axis], x_axis, y_axis)
    elif graph_type == 'table':
        figure = figures.serve_table_data(ds_df)

    elif graph_type == 'distribution':
        if len(x_axis) == 0:
            raise PreventUpdate
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

@app.callback(Output('div-graphs1', 'children'),
            [Input('dropdown-select-dataset', 'value'),
            Input('graph-select-update', 'value'),
            Input('dropdown-select-graph', 'value'),
            Input('graph-x-axis', 'value'),
            Input('graph-y-axis', 'value'),])
def update_graph_1(ds_name,
                selgraph,
                graph_type,
                x_axis,
                y_axis):
    
    if selgraph == 1:
        return update_graph_base(ds_name, graph_type, x_axis, y_axis)
    else:
        raise PreventUpdate

@app.callback(Output('div-graphs2', 'children'),
            [Input('dropdown-select-dataset', 'value'),
            Input('graph-select-update', 'value'),
            Input('dropdown-select-graph', 'value'),
            Input('graph-x-axis', 'value'),
            Input('graph-y-axis', 'value'),])
def update_graph_2(ds_name,
                selgraph,
                graph_type,
                x_axis,
                y_axis):
    
    if selgraph == 2:
        return update_graph_base(ds_name, graph_type, x_axis, y_axis)
    else:
        raise PreventUpdate

@app.callback(Output('div-graphs3', 'children'),
            [Input('dropdown-select-dataset', 'value'),
            Input('graph-select-update', 'value'),
            Input('dropdown-select-graph', 'value'),
            Input('graph-x-axis', 'value'),
            Input('graph-y-axis', 'value'),])
def update_graph_3(ds_name,
                selgraph,
                graph_type,
                x_axis,
                y_axis):
    
    if selgraph == 3:
        return update_graph_base(ds_name, graph_type, x_axis, y_axis)
    else:
        raise PreventUpdate

if __name__ == '__main__':
     app.run_server(debug=True)