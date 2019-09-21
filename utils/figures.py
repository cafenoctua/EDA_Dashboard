import colorlover as cl
import numpy as np

import plotly.graph_objs as go
import plotly.figure_factory as ff

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

def serve_table_data(ds_df):

    # Colorscale
    bright_cscale = [[0, '#FF0000'], [1, '#0000FF']]
    
    trace = go.Table(
        header=dict(values=ds_df.columns),
        cells=dict(values=[ds_df.loc[:, i] for i in ds_df.columns])
    )

    layout = go.Layout(
        margin=dict(l=100, r=100, t=100, b=100),
    )

    data = [trace]
    figure = go.Figure(data=data, layout=layout)

    return figure

def serve_dist_plot(ds_df,
                    ds_df_col_name):

    # Colorscale
    bright_cscale = [[0, '#FF0000'], [1, '#0000FF']]

    figure =ff.create_distplot([ds_df], [ds_df_col_name])

    # layout = go.Layout(
    #     hovermode='closest',
    #     legend=dict(x=0, y=-0.01, orientation="h"),
    #     margin=dict(l=100, r=100, t=100, b=100),
    # )

    # data = [trace]
    # figure = go.Figure(data=data, layout=layout)

    return figure