import requests
import sys
import re
from textblob import TextBlob

def req_facebook(req, token):
    r = requests.get("https://graph.facebook.com/v2.12/"+req, {'access_token':token})
    return r

def getResults(pageName, token):
    req = pageName+"?fields=posts.limit(10){message,comments.summary(true),likes.summary(true)}"
    results = req_facebook(req, token).json()
    return results

def getItems(results):
    messages = {}
    comments = {}
    commentCount = {}
    likes = {}
    for post in results['posts']['data']:
        i = 0
        mComments = []
        messages[post['id']] = post['message']
        for comment in post['comments']['data']:
            mComments.append(comment['message'])
        likes[post['id']] = post['likes']['summary']['total_count']
        comments[post['id']] = mComments
        commentCount[post['id']] = post['comments']['summary']['total_count']
    return messages, comments, commentCount, likes

def visualizationData(messages, comments, commentCount, likes):
    sentiments = {}
    for messageId in messages.keys():
        m = 0
        total = 0
        for comment in comments[messageId]:
            cc = re.sub(r"^https://t.co/[a-zA-Z0-9]*\s", " ", comment)
            cc = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*\s", " ", cc)
            cc = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*$", " ", cc)
            cc = cc.lower()
            cc = re.sub(r"that's","that is",cc)
            cc = re.sub(r"there's","there is",cc)
            cc = re.sub(r"what's","what is",cc)
            cc = re.sub(r"where's","where is",cc)
            cc = re.sub(r"it's","it is",cc)
            cc = re.sub(r"who's","who is",cc)
            cc = re.sub(r"i'm","i am",cc)
            cc = re.sub(r"she's","she is",cc)
            cc = re.sub(r"he's","he is",cc)
            cc = re.sub(r"they're","they are",cc)
            cc = re.sub(r"who're","who are",cc)
            cc = re.sub(r"ain't","am not",cc)
            cc = re.sub(r"wouldn't","would not",cc)
            cc = re.sub(r"shouldn't","should not",cc)
            cc = re.sub(r"can't","can not",cc)
            cc = re.sub(r"couldn't","could not",cc)
            cc = re.sub(r"won't","will not",cc)
            cc = re.sub(r"\W"," ",cc)
            cc = re.sub(r"\d"," ",cc)
            cc = re.sub(r"\s+[a-z]\s+"," ",cc)
            cc = re.sub(r"\s+[a-z]$"," ",cc)
            cc = re.sub(r"^[a-z]\s+"," ",cc)
            cc = re.sub(r"\s+"," ",cc)
            blob = TextBlob(cc)
            tot=0
            n=0
            for sentence in blob.sentences:
                tot+=sentence.sentiment.polarity
                n+=1
            if n > 0:
                total += tot/n
            else:
                total += tot
            m += 1
        if m>0:
            sentiments[messageId] = total/m
        else:
            sentiments[messageId] = total
    return messages, sentiments, commentCount, likes

def graphMain(pageName, token):
    results = getResults(pageName, token)
    messages, comments, commentCount, likes = getItems(results)
    return visualizationData(messages, comments, commentCount, likes)
