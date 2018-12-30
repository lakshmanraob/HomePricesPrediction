import json
import os
import datetime
import pytz

import tweepy
from dateutil import parser
from pymongo import MongoClient

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

MONGO_HOST = 'mongodb://localhost/TwiiterApi'


def connect_mongodb(username, created_at, tweet, re_tweet_count, place, location):
    client = MongoClient('localhost', 27017)
    db = client.TwiiterApi

    collection = db['twitterdb']

    # IST = pytz.timezone('Asia/Calcutta')
    tweet = {"username": username,
             "created_at": created_at,
             "tweet": tweet,
             "retweet_count": re_tweet_count,
             "place": place,
             "location": location}

    tweet_id = collection.insert_one(tweet).inserted_id

    print(tweet_id)


class StreamListener(tweepy.StreamListener):
    """
    This method will be called upon the successful connection with Twitter API
    """

    def on_connect(self):
        print("you are connected to twitter API")

    """
    Method get call when error occured
    """

    def on_error(self, status_code):
        if status_code != 200:
            print("Error found")
            return False

    """ 
    This menthod reads the data from the Twiter API
    """

    def on_data(self, data):
        try:
            raw_data = json.loads(data)

            if 'text' in raw_data:
                # print(raw_data)
                username = raw_data['user']['screen_name']
                date_time_obj = datetime.datetime.strptime(raw_data['created_at'],'%a %b %d %H:%M:%S %z %Y')
                timezone = pytz.timezone('Asia/Calcutta')
                print(date_time_obj.astimezone(timezone))
                created_at = date_time_obj.astimezone(timezone)
                tweet = raw_data['text']
                re_tweet_count = raw_data['retweet_count']

                if raw_data['place'] is not None:
                    place = raw_data['place']
                    print(place)
                else:
                    place = None

                location = raw_data['user']['location']

                connect_mongodb(username=username,
                                created_at=created_at,
                                tweet=tweet,
                                re_tweet_count=re_tweet_count,
                                place=place,
                                location=location)

        except EOFError as e:
            print(e)


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    listener = StreamListener(api=api)
    stream = tweepy.Stream(auth=auth,
                           listener=listener)

    track = ['cricket', 'Cricket']
    stream.filter(track=track,
                  languages=['en'])
