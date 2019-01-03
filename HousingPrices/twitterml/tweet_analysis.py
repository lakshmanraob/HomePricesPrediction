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
import numpy as np

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from textblob import TextBlob
from nltk.corpus import stopwords
import re

consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
access_token = 'access_token'
access_token_secret = 'access_token_secret'

MONGO_HOST = 'mongodb://localhost/TwiiterApi'

"""
For inserting the data into the Local mongodb http://localhost:27017/
"""


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
This class is meant for the twitterml stream, by default the time limit is given as 60 sec
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
        print("you are connected to twitterml API")

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
            print("Done with the twitterml pull")
            df = pd.DataFrame(self.tweet_data)
            tweet_object = TweetObject()
            clean_data = tweet_object.clean_tweets(df)
            print(clean_data.head())
            clean_data['sentiment'] = np.array([tweet_object.sentiment(x) for x in clean_data['clean_tweets']])
            tweet_object.word_cloud(clean_data)

            pos_tweets = [tweet for index, tweet in enumerate(clean_data["clean_tweets"]) if
                          clean_data["sentiment"][index] > 0]
            neg_tweets = [tweet for index, tweet in enumerate(clean_data["clean_tweets"]) if
                          clean_data["sentiment"][index] < 0]
            neu_tweets = [tweet for index, tweet in enumerate(clean_data["clean_tweets"]) if
                          clean_data["sentiment"][index] == 0]

            # Print results
            print(
                "percentage of positive tweets: {}%".format(100 * (len(pos_tweets) / len(clean_data['clean_tweets']))))
            print(
                "percentage of negative tweets: {}%".format(100 * (len(neg_tweets) / len(clean_data['clean_tweets']))))
            print("percentage of neutral tweets: {}%".format(100 * (len(neu_tweets) / len(clean_data['clean_tweets']))))

            # print(df.head())
            return False


"""
This class is meant for setting up the twitterml variables like
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


class TweetObject:
    def __init__(self, host=None, database=None):
        self.host = host
        self.database = database

    def mongo_connect(self):
        """
        connecting to Mongo data base and run the query

        in return it is going to give the Pandas dataFrame

        """
        client = MongoClient(self.host, 27017)
        db = client.TwiiterApi

        collection = db[self.database]

        myquery = {}

        my_data = collection.find(myquery)

        # for x in my_data:
        #     print(x)
        df = pd.DataFrame(list(my_data))
        return df

    def clean_tweets(self, df):
        """
        This method will clean the tweet details in the data frame by applying the following logics
        1. remove stopwords
        2. punctuations
        3. lower case
        4. html
        5. emoticons

        This will be done using Regex ? means option so colou?r matches	both color and colour.

        :param df:
        :return:
        """
        df.is_copy = False
        stopwords_list = stopwords.words('english')

        df['clean_tweets'] = None
        df['len'] = None

        for i in range(0, len(df['tweet'])):
            # get rid of anything which is not a letter
            exclusion_list = ['[^a-zA-Z]', 'rt', 'http', 'co', 'RT']
            exclusions = '|'.join(exclusion_list)
            text = re.sub(exclusions, ' ', df['tweet'][i])
            text = text.lower()
            words = text.split()
            words = [word for word in words if not word in stopwords_list]
            df['clean_tweets'][i] = ' '.join(words)

        # create column with data length
        df['len'] = np.array([len(tweet) for tweet in df["clean_tweets"]])

        return df

    def sentiment(self, tweet):
        """
        this method calculated the sentiment using textblob for polarity calculation

        :param tweet:
        :return:
        """

        analysis = TextBlob(tweet)

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity < 0:
            return -1
        else:
            return 0

    def save_to_csv(self, df):
        """
        method to save the cleaned data to csv for further analysis
        :param df:
        :return:
        """
        try:
            df.to_csv("clean_tweet.csv")
            print("\n")
            print("csv successfully saved. \n")
        except EOFError as e:
            print(e)

    def word_cloud(self, df):
        """
        for showing the word cloud graph
        :param df:
        :return:
        """
        plt.subplots(figsize=(12, 10))
        word_cloud = WordCloud(background_color='white',
                               width=500,
                               height=100).generate(" ".join(df['clean_tweets']))

        plt.imshow(word_cloud)
        plt.axis('off')
        plt.show()


"""
For getting the history tweet for the specified tag
"""


class TwitterHistory:
    def __init__(self, track):
        self.track = track
        self.tweet_data = []

    def get_history(self):
        print("in history")
        for tweet in tweepy.Cursor(api.search, q=self.track, rpp=100, lang='en').items(300):
            # for tweet in tweepy.Cursor(api.search, q=self.track, count=100, lang='en', result_type="recent").items(300):
            tweet_element = {}
            # print(tweet)
            print(tweet.created_at, tweet.text)
            username = tweet.user.screen_name  # raw_data['user']['screen_name']
            # date_time_obj = datetime.datetime.strptime(tweet.created_at, '%Y-%m-%d %H:%M:%S')
            # timezone = pytz.timezone('Asia/Calcutta')
            # print(date_time_obj.astimezone(timezone))
            # created_at = date_time_obj.astimezone(timezone)
            created_at = tweet.created_at
            tweet_text = tweet.text
            re_tweet_count = tweet.retweet_count

            if tweet.place is not None:
                place = tweet.place
                print(place)
            else:
                place = None

            location = tweet.user.location

            tweet_element['username'] = username
            tweet_element['created_at'] = created_at
            tweet_element['tweet'] = tweet_text
            tweet_element['re_tweet_count'] = re_tweet_count
            tweet_element['place'] = place
            tweet_element['location'] = location

            self.tweet_data.append(tweet_element)

    def history_analysis(self):
        print("In history analysis")
        df = pd.DataFrame(self.tweet_data)
        tweet_object = TweetObject()
        clean_data = tweet_object.clean_tweets(df)
        print(clean_data.head())
        clean_data['sentiment'] = np.array([tweet_object.sentiment(x) for x in clean_data['clean_tweets']])
        tweet_object.word_cloud(clean_data)

        pos_tweets = [tweet for index, tweet in enumerate(clean_data["clean_tweets"]) if
                      clean_data["sentiment"][index] > 0]
        neg_tweets = [tweet for index, tweet in enumerate(clean_data["clean_tweets"]) if
                      clean_data["sentiment"][index] < 0]
        neu_tweets = [tweet for index, tweet in enumerate(clean_data["clean_tweets"]) if
                      clean_data["sentiment"][index] == 0]

        # Print results
        print("percentage of positive tweets: {}%".format(100 * (len(pos_tweets) / len(clean_data['clean_tweets']))))
        print("percentage of negative tweets: {}%".format(100 * (len(neg_tweets) / len(clean_data['clean_tweets']))))
        print("percentage of neutral tweets: {}%".format(100 * (len(neu_tweets) / len(clean_data['clean_tweets']))))


if __name__ == '__main__':
    # creating the object for setting up the environment variables
    env_set_up = SetUpEnvironmentVariables('settings.json')
    data = env_set_up.extract_data()

    auth = tweepy.OAuthHandler(data[consumer_key], data[consumer_secret])
    auth.set_access_token(data[access_token], data[access_token_secret])

    api = tweepy.API(auth, wait_on_rate_limit=True)
    track = ['Modi2019Interview']
    # track = ['Cricket']

    # # creating the listener
    # listener = StreamListener(time_limit=30, twitter_track=track)
    # stream = tweepy.Stream(auth=auth,
    #                        listener=listener)
    #
    # stream.filter(track=track,
    #               languages=['en'])

    tweet_history = TwitterHistory(track=track)
    tweet_history.get_history()
    tweet_history.history_analysis()
