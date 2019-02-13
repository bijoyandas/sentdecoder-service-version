from utils.tweet_sentiment import sentiment_for_tweets
from utils.summarizer import getSummaryMain
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import nltk

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
port = int(os.getenv("PORT"))
CORS(app)

@app.route('/twitter/sentiment', methods=['POST'])
def get_tweet_sentiment():
    data = json.loads(request.get_data())
    query = data['query']
    limit = int(data['limit'])
    country = data['country']
    area = int(data['area'])

    if country is "none":
        country = None
    if area is 0:
        area = 500

    sentiment_list = sentiment_for_tweets(query, limit, country, area)
    return jsonify(
        status=200,
        results=sentiment_list
    )

@app.route('/article/summary', methods=['POST'])
def get_summary_and_sentiment():
    data = json.loads(request.get_data())
    url = data['url']
    summary, polarity = getSummaryMain(url)
    return jsonify(
        status=200,
        results={
            "sentences":summary,
            "polarity":polarity
        }
    )

app.run(host='0.0.0.0', port=port)
