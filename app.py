import dash
import dash_core_components as dcc
import dash_html_components as html

import utils.dash_reuable_components as drc

app = dash.Dash(__name__)
server = app.server

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

    html.Div(id='body', className='UI container', children=[
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
                        drc.Card([
                            drc.NamedDropdown(
                                name='Select Dataset',
                                id='dropdown-select-dataset',
                                options=[
                                    {'label': 'Iris', 'value': 'iris'},
                                    {'label': 'Boston house-prices', 'value': 'boston house-prices'},
                                ],
                                clearable=False,
                                searchable=False,
                                value='iris'
                            ),
                        ]),
                        drc.Card([
                            drc.NamedDropdown(
                                name='Select Graph',
                                id='dropdown-select-graph',
                                options=[
                                    {'label': 'Scatter', 'value': 'scatter'},
                                    {'label': 'Histogram', 'value': 'histogram'},
                                ],
                                clearable=False,
                                searchable=False,
                                value='scatter'
                            ),
                        ])
                    ]),
                    drc.Card([
                        drc.NamedDropdown(
                            name='X-axis',
                            id='graph-x-axis',
                            options=[
                                ''
                            ],
                            clearable=False,
                            searchable=False,
                            value=''
                        ),
                        drc.NamedDropdown(
                            name='Y-axis',
                            id='graph-y-axis',
                            options=[
                                ''
                            ],
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