import tweepy
import os
import re
import pandas as pd
import streamlit as st
import nltk
from nltk.corpus import stopwords
from collections import Counter

st.subheader('Ticker bot v0')
user_input = st.text_input("User Handle","UniswapD")
api_key = "3m9Hy3HVG7wKNvOuz3hiliQL9"
api_secret = "8pQnb6fpeu1czGYYGO02HUsyOtsNKh6XIUoTnZZGxj7stFd2OI"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAKdZNgEAAAAAnRMAHs9gpDs9HMdKhXkrRVP7wEs%3DupliQXeSnLkGpb3cv0YdgHuqH9iEGvUpVCvg6Dc56WURAmxafv"

auth = tweepy.AppAuthHandler(api_key, api_secret)

stop_words = set(stopwords.words('english'))
words = set(nltk.corpus.words.words())

crypto_stop_words= ["guys","nft","buys","lets","haha","ath","gems","defi","bags", "gtfo", "apy","jpeg","fees" ,"fuck" ,"ups", "ines", "shit" ,"alt","buy","more","bois",
                    ]

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

#query_name = "UniswapD"


all_text = " "

statuses = api.user_timeline(user_input, count = 50) 
  
# printing the statuses 
for status in statuses: 
    #print(status.text, end = "\n\n")
    st.text(status.text)
    all_text = all_text + " " + status.text


def ticker_cleaner(all_text):
  ticker = re.findall("[$]\w+", all_text)
  ticker2 = re.findall(r"\b\w{3,4}\b", all_text)
  x = [w .strip() for w in ticker2 \

          if w.lower() not in words or not w.isalpha()]

  y = [w .strip() for w in x \

          if w.lower() not in crypto_stop_words]

  z = [w .strip() for w in y \

          if w.lower() not in stop_words]

  ticker.extend(z)
  
  final_ticker = []
  for t in ticker:
    temp = t.lower()
    temp = temp.replace("$","")
    if len(temp) > 2 and not any(chr.isdigit() for chr in temp):
      final_ticker.append(temp)
  
  return final_ticker



all_text2 = all_text
ticker = ticker_cleaner(all_text)

letter_counts = Counter(ticker)
df = pd.DataFrame.from_dict(letter_counts, orient='index')
df.plot(kind='bar')

st.bar_chart(df)
