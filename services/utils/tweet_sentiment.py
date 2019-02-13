import re
from utils.twitter_operations import get_tweet_list, get_tweet_for_country
from textblob import TextBlob

def sentiment_for_tweets(query, limit, country=None, area=500):
    if country is None:
        list_tweets = get_tweet_list(query, limit)
    else:
        list_tweets = get_tweet_for_country(query, limit, country, area)
    tweet_sentiment_list = []
    for t in list_tweets:
        tweet_sentiment_dict = {}
        tweet = t
        tweet = re.sub(r"^https://t.co/[a-zA-Z0-9]*\s", " ", t)
        tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*\s", " ", tweet)
        tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*$", " ", tweet)
        tweet = tweet.lower()
        tweet = re.sub(r"that's","that is",tweet)
        tweet = re.sub(r"there's","there is",tweet)
        tweet = re.sub(r"what's","what is",tweet)
        tweet = re.sub(r"where's","where is",tweet)
        tweet = re.sub(r"it's","it is",tweet)
        tweet = re.sub(r"who's","who is",tweet)
        tweet = re.sub(r"i'm","i am",tweet)
        tweet = re.sub(r"she's","she is",tweet)
        tweet = re.sub(r"he's","he is",tweet)
        tweet = re.sub(r"they're","they are",tweet)
        tweet = re.sub(r"who're","who are",tweet)
        tweet = re.sub(r"ain't","am not",tweet)
        tweet = re.sub(r"wouldn't","would not",tweet)
        tweet = re.sub(r"shouldn't","should not",tweet)
        tweet = re.sub(r"can't","can not",tweet)
        tweet = re.sub(r"couldn't","could not",tweet)
        tweet = re.sub(r"won't","will not",tweet)
        tweet = re.sub(r"\W"," ",tweet)
        tweet = re.sub(r"\d"," ",tweet)
        tweet = re.sub(r"\s+[a-z]\s+"," ",tweet)
        tweet = re.sub(r"\s+[a-z]$"," ",tweet)
        tweet = re.sub(r"^[a-z]\s+"," ",tweet)
        tweet = re.sub(r"\s+"," ",tweet)
        blob = TextBlob(tweet)
        sum=0
        n=0
        for sentence in blob.sentences:
            sum+=sentence.sentiment.polarity
            n+=1
        sent = round(sum/n,4)
        tweet_sentiment_dict['tweet'] = t
        tweet_sentiment_dict['sentiment'] = sent
        tweet_sentiment_list.append(tweet_sentiment_dict)
    return tweet_sentiment_list
