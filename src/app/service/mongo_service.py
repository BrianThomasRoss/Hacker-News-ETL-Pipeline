# -*- coding: utf-8 -*-
"""Handles interactions with MongoDB."""
import pymongo
import pandas as pd


class MongoService(object):

    def __init__(self) -> None:

        self._client = pymongo.MongoClient('localhost', 27017)
        self._db = self._client.twitter_election_sentiment
        self._collection = self._db.tweet_info

    def create_tweet_dataframe(self):
        """Return a pandas DataFrame from mongo collection"""
        return pd.DataFrame(list(self._collection.find()))

    @property
    def recent_tweets_data(self):
        """"""
        df = self.create_tweet_dataframe()

        values = [[date for date in df.head(5)['creation_datetime']],
                  [text for text in df.head(5)['text']],
                  [senti_val for senti_val in df.head(5)['senti_val']],
                  [subjectivity for subjectivity in df.head(5)['subjectivity']]]

        return values

    @property
    def most_active_data(self):
        """"""
        df = self.create_tweet_dataframe()
        df['user_description'] = df['user_description'].fillna('')
        df['user'] = df['username'] + df['user_description']
        df['usercount'] = df.groupby('user')['user'].transform('count')
        df.usercount = df.usercount.astype('int64')
        result = df[['username',
                     'user_description',
                     'usercount']].drop_duplicates()
        result = result.sort_values(by=['usercount'], ascending=False).head(10)
        result = result.sort_values(by=['usercount'])

        return result

    @property
    def daily_tweets_data(self):
        """"""
        """"""
        df = self.create_tweet_dataframe()

        # sort tweets by descending follower count
        df['creation_date'] = pd.to_datetime(df['creation_datetime'])
        df['tweet_date'] = pd.DatetimeIndex(df['creation_date']).date
        df_2 = df.groupby(['tweet_date']).username.count().reset_index()
        df_2.rename(columns={'username': 'users_count'})

        return df_2

    @property
    def overall_sentiment_data(self):
        """"""
        df = self.create_tweet_dataframe()
        cat_senti = []

        for row in df.senti_val:
            if float(row) > 0.3:
                cat_senti.append('Positive')
            elif float(row) < -0.3:
                cat_senti.append('Negative')
            else:
                cat_senti.append('Neutral')

        df['cat_senti'] = cat_senti

        def cal_percent(senti):
            count_net = len(df[df['cat_senti'] == senti])
            return count_net

        data = [cal_percent('Neutral'),
                cal_percent('Positive'),
                cal_percent('Negative')
                ]

        return data
