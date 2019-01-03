import os
import re
import pandas as pd

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob

from pymongo import MongoClient


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
                               width=1000,
                               height=100).generate(" ".join(df['clean_tweets']))

        plt.imshow(word_cloud)
        plt.axis('off')
        plt.show()


if __name__ == '__main__':
    # nltk.download('stopwords')

    tw = TweetObject('localhost', 'twitterdb')
    data_frame = tw.mongo_connect()

    data = tw.clean_tweets(data_frame)

    data['sentiment'] = np.array([tw.sentiment(x) for x in data['clean_tweets']])
    tw.word_cloud(data)
    tw.save_to_csv(data)

    pos_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["sentiment"][index] > 0]
    neg_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["sentiment"][index] < 0]
    neu_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["sentiment"][index] == 0]

    # Print results
    print("percentage of positive tweets: {}%".format(100 * (len(pos_tweets) / len(data['clean_tweets']))))
    print("percentage of negative tweets: {}%".format(100 * (len(neg_tweets) / len(data['clean_tweets']))))
    print("percentage of neutral tweets: {}%".format(100 * (len(neu_tweets) / len(data['clean_tweets']))))
