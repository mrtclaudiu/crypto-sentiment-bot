import pandas as pd
import numpy as np
import requests
from ta import add_all_ta_features
from ta.utils import dropna
from textblob import TextBlob

# Funcție pentru a calcula indicatorii tehnici folosind TA-Lib
def calculate_technical_indicators(data):
    data = dropna(data)
    data = add_all_ta_features(
        data, open="open", high="high", low="low", close="close", volume="volume", fillna=True
    )
    return data

# Funcție pentru a colecta date fundamentale folosind Alpha Vantage API
def get_fundamental_data(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame([data])
    return df

# Funcție pentru a colecta date de sentiment de pe Twitter folosind Tweepy
def get_twitter_sentiment(query, api_key, api_secret_key, access_token, access_token_secret):
    import tweepy

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweets = api.search_tweets(q=query, count=100)
    sentiments = []

    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        sentiments.append(analysis.sentiment.polarity)

    return np.mean(sentiments)

# Funcție principală pentru a colecta și integra toate datele
def main():
    # Exemplu de date istorice de preț și volum
    data = pd.read_csv('historical_data.csv')

    # Calcularea indicatorilor tehnici
    data = calculate_technical_indicators(data)

    # Colectarea datelor fundamentale
    fundamental_data = get_fundamental_data('AAPL', 'YOUR_ALPHA_VANTAGE_API_KEY')

    # Colectarea datelor de sentiment de pe Twitter
    twitter_sentiment = get_twitter_sentiment('AAPL', 'YOUR_TWITTER_API_KEY', 'YOUR_TWITTER_API_SECRET_KEY', 'YOUR_TWITTER_ACCESS_TOKEN', 'YOUR_TWITTER_ACCESS_TOKEN_SECRET')

    # Integrarea datelor fundamentale și de sentiment în setul de date principal
    data['twitter_sentiment'] = twitter_sentiment
    for col in fundamental_data.columns:
        data[col] = fundamental_data[col].iloc[0]

    # Salvarea setului de date integrat
    data.to_csv('integrated_data.csv', index=False)

if __name__ == "__main__":
    main()
