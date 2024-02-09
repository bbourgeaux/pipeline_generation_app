import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import textblob
from collections import Counter

# Load sentiment analysis results
sentiment_analysis_results = pd.read_csv('sentiment_analysis_results.txt')

# Perform crypto market analysis
crypto_market_analysis_results = {}
for coin in sentiment_analysis_results['coin']:
    sentiment_score = sentiment_analysis_results['sentiment_score'][sentiment_analysis_results['coin'] == coin]
    if sentiment_score.mean() > 0.5:
        crypto_market_analysis_results[coin] = 'positive'
    elif sentiment_score.mean() < -0.5:
        crypto_market_analysis_results[coin] = 'negative'
    else:
        crypto_market_analysis_results[coin] = 'neutral'

# Save crypto market analysis results
crypto_market_analysis_results_df = pd.DataFrame(crypto_market_analysis_results.items(), columns=['coin', 'market_analysis'])
crypto_market_analysis_results_df.to_csv('crypto_market_analysis_results.txt', index=False)

