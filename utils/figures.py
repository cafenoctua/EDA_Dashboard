import colorlover as cl
import plotly.graph_objs as go
import numpy as np

def serve_scatter_plot(x_data,
                        y_data,
                        x_col_name,
                        y_col_name):

    # Colorscale
    bright_cscale = [[0, '#FF0000'], [1, '#0000FF']]

    trace = go.Scatter(
        x=x_data,
        y=y_data,
        mode='markers',
        name=f'{y_col_name}',
        marker=dict(
            size=10,
            color=y_data,
            colorscale=bright_cscale,
            line=dict(
                width=1
            )
        )
    )

    layout = go.Layout(
        xaxis=dict(
            showticklabels=True,
            showgrid=True,
            zeroline=False,
            showline=True,
        ),
        yaxis=dict(
            showticklabels=True,
            showgrid=True,
            zeroline=False,
            showline=True,
        ),
        hovermode='closest',
        legend=dict(x=0, y=-0.01, orientation="h"),
        margin=dict(l=100, r=100, t=100, b=100),
    )

    data = [trace]
    figure = go.Figure(data=data, layout=layout)

    return figure