# -*- coding:utf-8 -*-
"""Primary endpoint for the API."""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer(object):

    _vader = SentimentIntensityAnalyzer()

    def
