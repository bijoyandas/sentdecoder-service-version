import tweepy
from tweepy import OAuthHandler
import pickle
from utils import constants

def get_api():
    auth = OAuthHandler(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
    auth.set_access_token(constants.ACCESS_TOKEN, constants.ACCESS_SECRET)
    api = tweepy.API(auth,timeout=10)
    return api

def get_tweet_list(query, limit):
    api = get_api()
    list_tweets = []
    for status in tweepy.Cursor(api.search,q=query+" -filter:retweets",lang='en',result_type='recent').items(limit):
        list_tweets.append(status.text)
    return list_tweets

def get_tweet_for_country(query, limit, country, area = 500):
    api = get_api()
    list_tweets = []
    with open("utils/resources/geomapping.pickle","rb") as f:
        country_map = pickle.load(f)
    country = country.lower()
    if country not in country_map.values():
        for status in tweepy.Cursor(api.search, q=query+" "+country+" -filter:retweets",lang='en',result_type='recent').items(limit):
            list_tweets.append(status.text)
    else:
        for status in tweepy.Cursor(api.search, q=query+" -filter:retweets",lang='en',result_type='recent',geocode=country_map[country]+","+area+"km").items(limit):
            list_tweets.append(status.text)
    return list_tweets
