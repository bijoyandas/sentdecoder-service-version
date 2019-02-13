# Importing the libraries
import bs4 as bs
import urllib.request
import re
import nltk
import heapq
import sys
from textblob import TextBlob

def getText(url):
    # Getting the data source
    source = urllib.request.urlopen(url).read()

    # Parsing the data/ creating BeautifulSoup object
    soup = bs.BeautifulSoup(source,'lxml')

    # Fetching the data
    text = ""
    for paragraph in soup.find_all('p'):
        text += paragraph.text
    return text

def getCleanedText(sourceText):
    # Preprocessing the data
    sourceText = re.sub(r'\[[0-9]*\]',' ',sourceText)
    sourceText = re.sub(r'\s+',' ',sourceText)

    cleanText = sourceText.lower()
    cleanText = re.sub(r'\W',' ',cleanText)
    cleanText = re.sub(r'\d',' ',cleanText)
    cleanText = re.sub(r'\s+',' ',cleanText)
    return sourceText, cleanText

def getSummary(text, cleanText):
    # Tokenize sentences
    sentences = nltk.sent_tokenize(text)

    # Stopword list
    stop_words = nltk.corpus.stopwords.words('english')

    # Word counts
    word2count = {}
    for word in nltk.word_tokenize(cleanText):
        if word not in stop_words:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1

    # Converting counts to weights
    for key in word2count.keys():
        word2count[key] = word2count[key]/max(word2count.values())

    # Product sentence scores
    sent2score = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word2count.keys():
                if len(sentence.split(' ')) < 50:
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = 0
                    else:
                        sent2score[sentence] += word2count[word]

    # Gettings best 5 lines
    best_sentences = heapq.nlargest(5, sent2score, key=sent2score.get)

    count = 0
    total=0
    n=0
    summary = []
    for sentence in best_sentences:
        cs = re.sub(r"^https://t.co/[a-zA-Z0-9]*\s", " ", sentence)
        cs = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*\s", " ", cs)
        cs = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*$", " ", cs)
        cs = cs.lower()
        cs = re.sub(r"that's","that is",cs)
        cs = re.sub(r"there's","there is",cs)
        cs = re.sub(r"what's","what is",cs)
        cs = re.sub(r"where's","where is",cs)
        cs = re.sub(r"it's","it is",cs)
        cs = re.sub(r"who's","who is",cs)
        cs = re.sub(r"i'm","i am",cs)
        cs = re.sub(r"she's","she is",cs)
        cs = re.sub(r"he's","he is",cs)
        cs = re.sub(r"they're","they are",cs)
        cs = re.sub(r"who're","who are",cs)
        cs = re.sub(r"ain't","am not",cs)
        cs = re.sub(r"wouldn't","would not",cs)
        cs = re.sub(r"shouldn't","should not",cs)
        cs = re.sub(r"can't","can not",cs)
        cs = re.sub(r"couldn't","could not",cs)
        cs = re.sub(r"won't","will not",cs)
        cs = re.sub(r"\W"," ",cs)
        cs = re.sub(r"\d"," ",cs)
        cs = re.sub(r"\s+[a-z]\s+"," ",cs)
        cs = re.sub(r"\s+[a-z]$"," ",cs)
        cs = re.sub(r"^[a-z]\s+"," ",cs)
        cs = re.sub(r"\s+"," ",cs)
        blob = TextBlob(cs)
        for s in blob.sentences:
            total+=s.sentiment.polarity
            n+=1
        summary.append(sentence)
    polarity = total/n
    return summary, polarity

def getSummaryMain(url):
    sourceText = getText(url)
    text, cleanText = getCleanedText(sourceText)
    summary, polarity = getSummary(text, cleanText)
    return summary, polarity
