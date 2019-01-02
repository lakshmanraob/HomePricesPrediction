import json
import os
import datetime
import pytz

import tweepy
from dateutil import parser
from pymongo import MongoClient
from pathlib import Path
import time
import pandas as pd

consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
access_token = 'access_token'
access_token_secret = 'access_token_secret'

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


"""
This class is meant for the twitter stream, by default the time limit is given as 60 sec
Can be increased based on the time you send as parameter
"""


class StreamListener(tweepy.StreamListener):
    def __init__(self, time_limit=60, twitter_track=["Twitter"]):
        self.start_time = time.time()
        self.time_limit = time_limit
        self.track = twitter_track
        self.tweet_data = []

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
        if time.time() - self.start_time < self.time_limit:
            tweet_element = {}
            try:
                raw_data = json.loads(data)

                if 'text' in raw_data:
                    # print(raw_data)
                    username = raw_data['user']['screen_name']
                    date_time_obj = datetime.datetime.strptime(raw_data['created_at'], '%a %b %d %H:%M:%S %z %Y')
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

                    tweet_element['username'] = username
                    tweet_element['created_at'] = created_at
                    tweet_element['tweet'] = tweet
                    tweet_element['re_tweet_count'] = re_tweet_count
                    tweet_element['place'] = place
                    tweet_element['location'] = location

                    self.tweet_data.append(tweet_element)
                    # connect_mongodb(username=username,
                    #                 created_at=created_at,
                    #                 tweet=tweet,
                    #                 re_tweet_count=re_tweet_count,
                    #                 place=place,
                    #                 location=location)
            except EOFError as e:
                print(e)
                return False
            return True
        else:
            print("Done with the twitter pull")
            df = pd.DataFrame(self.tweet_data)
            print(df.head())
            return False


"""
This class is meant for setting up the twitter variables like
consumer key etc
"""


class SetUpEnvironmentVariables:
    def __init__(self, file_name):
        self.file_name = file_name

    def extract_data(self):
        script_location = Path(__file__).absolute().parent
        print(script_location)
        with open(script_location / self.file_name, encoding='utf-8') as setting_file:
            data = json.loads(setting_file.read())
        return data


if __name__ == '__main__':
    # creating the object for setting up the environment variables
    env_set_up = SetUpEnvironmentVariables('settings.json')
    data = env_set_up.extract_data()

    auth = tweepy.OAuthHandler(data[consumer_key], data[consumer_secret])
    auth.set_access_token(data[access_token], data[access_token_secret])

    api = tweepy.API(auth, wait_on_rate_limit=True)
    track = ['Modi2019Interview']

    # creating the listener
    listener = StreamListener(time_limit=30, twitter_track=track)
    stream = tweepy.Stream(auth=auth,
                           listener=listener)

    stream.filter(track=track,
                  languages=['en'])
