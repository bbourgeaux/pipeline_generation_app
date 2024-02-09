
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Load the sentiment analysis results from a file
sentiment_analysis_results = pd.read_csv('sentiment_analysis_results.txt')

# Perform sentiment analysis on each cryptocurrency
for i in range(sentiment_analysis_results.shape[0]):
    analysis = TextBlob(sentiment_analysis_results.iloc[i]['text'])
    sentiment = analysis.sentiment.polarity
    sentiment_analysis_results.iloc[i]['sentiment'] = sentiment

# Vectorize the sentiment analysis results
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sentiment_analysis_results['text'])

# Train a Naive Bayes classifier on the sentiment analysis results
clf = MultinomialNB()
clf.fit(X, sentiment_analysis_results['sentiment'])

# Use the classifier to predict the sentiment of new cryptocurrencies
new_cryptocurrencies = ['Bitcoin', 'Ethereum', 'Ripple']
predicted_sentiments = clf.predict(vectorizer.transform(new_cryptocurrencies))

# Analyze the crypto market based on the predicted sentiment
positive_cryptos = []
negative_cryptos = []
neutral_cryptos = []

for crypto in new_cryptocurrencies:
    if predicted_sentiments[new_cryptocurrencies.index(crypto)] == 1:
        positive_cryptos.append(crypto)
    elif predicted_sentiments[new_cryptocurrencies.index(crypto)] == -1:
        negative_cryptos.append(crypto)
    else:
        neutral_cryptos.append(crypto)

# Generate a report on the crypto market analysis
report = f"Crypto Market Analysis:\n\n"
report += f"Positive Cryptocurrencies: {', '.join(positive_cryptos)}\n"
report += f"Negative Cryptocurrencies: {', '.join(negative_cryptos)}\n"
report += f"Neutral Cryptocurrencies: {', '.join(neutral_cryptos)}\n"

# Save the report to a file
crypto_market_analysis_results = pd.DataFrame({'report': [report]})
crypto_market_analysis_results.to_csv('crypto_market_analysis_results.txt', index=False)

