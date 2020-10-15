# -*- coding: utf-8 -*-
"""Define application callbacks here."""
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

from app.service import MongoService
from .page import index


def wrap_callbacks(app):
    @app.callback(Output('recent-tweets-table', 'figure'),
                  [Input('interval-component', 'n_intervals')])
    def update_graph_live(n):
        mng = MongoService()
        values = mng.recent_tweets_data

        trace0 = go.Table(
            columnorder=[1, 2, 3, 4],
            columnwidth=[15, 60, 15, 15],
            header=dict(
                values=[['<b>Date</b>'], ['<b>Text</b>'],
                        ['<b>Sentiment Score</b>'], ['<b>Subjectivity Score</b>']],
                line=dict(color='blue'),
                fill=dict(color='#1B95E0'),
                align=['left', 'center'],
                font=dict(color='white', size=16),
                height=40
            ),
            cells=dict(
                values=values,
                line=dict(color='blue'),
                fill=dict(color=['white']),
                align=['left', 'center'],
                font=dict(color='black', size=14),
                height=30
            ))

        data = [trace0]
        layout = dict(title='<b>Most Recent Election Tweets</b>',
                      height=700,
                      titlefont=dict(size=20))

        fig = dict(data=data, layout=layout)

        return fig

    @app.callback(Output('tweets-per-day', 'figure'),
                  [Input('interval-component', 'n_intervals')])
    def tweets_per_day(n):
        mng = MongoService()
        df = mng.daily_tweets_data

        trace1 = go.Bar(
            x=df['tweet_date'],
            y=df['username'],
            name='Tweets per Day',
            marker=dict(color='#1B95E0')  # set the marker color to gold
        )

        data = [trace1]

        layout = go.Layout(
            title='<b>Tweets per day</b>',
            barmode='group',
            titlefont=dict(size=20)
        )

        fig = go.Figure(data=data, layout=layout)

        return fig

    @app.callback(Output('most-active-users', 'figure'),
                  [Input('interval-component', 'n_intervals')])
    def most_active_users(n):
        # connect to mongo and store in pandas dataframe
        mng = MongoService()
        df = mng.most_active_data

        data = [go.Bar(
            x=df['usercount'],
            y=df['username'],
            marker={'color': ['rgb(26, 118, 255)', 'rgb(26, 118, 255)',
                              'rgb(26, 118, 255)', 'rgb(26, 118, 255)', 'rgb(26, 118, 255)',
                              'rgb(26, 118, 255)', 'rgb(26, 118, 255)', 'rgb(26, 118, 255)', 'blue', 'red']},
            text=df['user_description'],
            orientation='h',
        )]

        layout = dict(title='<b>Most Active Users Tweeting</b>', height=700,
                      titlefont=dict(size=20))

        fig = dict(data=data, layout=layout)

        return fig

    @app.callback(Output('donut-sentiment', 'figure'),
                  [Input('interval-component', 'n_intervals')])
    def donut_sentiment(n):
        # connect to mongo and store in pandas dataframe
        mng = MongoService()
        data = mng.overall_sentiment_data

        ## Donut plot
        trace1 = {"hole": 0.5,
                  "type": "pie",
                  "labels": ["Neutral",
                             "Positive",
                             "Negative"
                             ],
                  "values": data,
                  "showlegend": True,
                  "marker.line.width": 10,
                  "marker.line.color": 'white',
                  'marker': {'colors': ['grey',
                                        'green',
                                        'red'
                                        ]
                             }
                  }

        layout = go.Layout(
            title="<b>Sentimental analysis</b>",
            titlefont=dict(size=20),
            height=600)

        fig = go.Figure(data=[trace1], layout=layout)

        return fig
