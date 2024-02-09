
import sentiment_analysis
import pandas as pd
from collections import Counter

def top_crypto_trends(sentiment_analysis):
    sentiment_scores = sentiment_analysis.get_sentiment_scores()
    crypto_sentiment = sentiment_scores['crypto']
    top_trends = crypto_sentiment.most_common(10)
    trend_names = [trend[0] for trend in top_trends]
    crypto_trends = pd.DataFrame({'Trends': trend_names})
    return crypto_trends

crypto_trends = top_crypto_trends(sentiment_analysis)
crypto_trends.to_csv('crypto_trends.ext', index=False)

