import pymongo
from pymongo import MongoClient
import datetime
import pytz

client = MongoClient('localhost', 27017)
db = client.TwiiterApi

collection = db['twitterdb']

IST = pytz.timezone('Asia/Calcutta')
tweet = {"username": "lakshman", "date": datetime.datetime.now(tz=IST)}

tweet_id = collection.insert_one(tweet).inserted_id

print(tweet_id)
