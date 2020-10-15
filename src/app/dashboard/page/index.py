# -*- coding: utf-8 -*-
""""""
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(children=[
    html.Div([
        html.Div(
            dcc.Graph(
                id='recent-tweets-table',
            ), style={'display': 'inline-block', 'width': '60%'}),
        html.Div(
            dcc.Graph(
                id='most-active-users',
            ), style={'display': 'inline-block', 'width': '40%'}),
        html.Div(
            dcc.Interval(
                id='interval-component',
                interval=30 * 1000,  # in milliseconds
                n_intervals=0
            ))]
        , style={'width': '100%', 'display': 'inline-block'}
    ),
    html.Div([
        html.Div(
            dcc.Graph(
                id='tweets-per-day',
            ), style={'display': 'inline-block', 'vertical-align': 'top', 'width': '50%'}),
        html.Div(
            dcc.Graph(
                id='donut-sentiment',
            ), style={'display': 'inline-block', 'width': '50%'})]
        , style={'width': '100%', 'display': 'inline-block'}
    )
])
