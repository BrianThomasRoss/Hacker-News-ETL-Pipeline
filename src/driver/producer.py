# -*- coding:utf-8 -*-
""""""
import json
# import requests
import configparser
from typing import Dict, List

import pykafka
from textblob import TextBlob
from tweepy import OAuthHandler, Stream, StreamListener

twitter_cfg = configparser.ConfigParser()
twitter_cfg.read_file(open('twitter.cfg'))

# kafka_cfg = configparser.ConfigParser()
# kafka_cfg.read_file(open('kafka.cfg'))

# _CONNECTION_STRING = kafka_cfg.get('BOOTSTRAP_SERVERS', 'TLS_CONNECTION_STRING')


class TweetListener(StreamListener):
    """Producer class.

    Reads stream of incoming tweets using TweePy's StreamListener class,
    parse response object to ensure hygienic data, then using TextBlob
    performs simple sentiment analysis on contents of the tweet body and
    constructs a JSON object to dispatch to Kafka broker.
    """

    def __init__(self):
        self.client = pykafka.KafkaClient("localhost:9092")
        self.producer = self.client.topics[bytes(
            'electionSentimentTwitterStream', 'ascii'
        )].get_producer()

    # parse json tweet object stream to get desired data
    def on_data(self, data):
        try:
            json_data = json.loads(data)
            send_data = '{}'
            json_send_data = json.loads(send_data)

            # make checks for retweet and extended tweet-->done for truncated text
            if "retweeted_status" in json_data:
                try:
                    json_send_data['text'] = json_data['retweeted_status']['extended_tweet']['full_text']
                except:
                    json_send_data['text'] = json_data['retweeted_status']['text']
            else:
                try:
                    json_send_data['text'] = json_data['extended_tweet']['full_text']
                except:
                    json_send_data['text'] = json_data['text']


            json_send_data['creation_datetime'] = json_data['created_at']
            json_send_data['username'] = json_data['user']['name']
            json_send_data['location'] = json_data['user']['location']
            json_send_data['userDescr'] = json_data['user']['description']
            json_send_data['followers'] = json_data['user']['followers_count']
            json_send_data['retweets'] = json_data['retweet_count']
            json_send_data['favorites'] = json_data['favorite_count']

            blob = TextBlob(json_send_data['text'])
            (json_send_data['senti_val'], json_send_data['subjectivity']) = blob.sentiment


            # check for this really small value and make it 0
            if json_send_data['senti_val'] == 1.6653345369377347e-17:
                json_send_data['senti_val'] = 0
            # keep only the first two decimal points of sentiment value and subjectivity
            json_send_data['senti_val'] = str(json_send_data['senti_val'])[:4]
            json_send_data['subjectivity'] = str(json_send_data['subjectivity'])[:4]

            print(json_send_data)            # print(json_send_data['location'])

            # push data to producer
            self.producer.produce(bytes(json.dumps(json_send_data), 'ascii'))
            return True
        except KeyError:
            return True

    def on_error(self, status):
        print(status)
        return True


if __name__ == "__main__":
    words = ['2020 election', 'biden', 'trump', 'vote 2020', 'us elections']

    consumer_key = twitter_cfg.get('AUTH', 'CONSUMER_KEY')
    consumer_secret = twitter_cfg.get('AUTH', 'CONSUMER_SECRET')
    access_token = twitter_cfg.get('AUTH', 'ACCESS_TOKEN')
    access_secret = twitter_cfg.get('AUTH', 'ACCESS_SECRET')

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # create AFINN object for sentiment analysis
    # afinn = Afinn(emoticons=True)

    # perform activities on stream
    twitter_stream = Stream(auth, TweetListener(), tweet_mode='extended')
    twitter_stream.filter(track=words)
