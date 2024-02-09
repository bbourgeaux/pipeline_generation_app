import pandas as pd
import numpy as np
import re
import os

# Read the input files
silicon_valley_news = pd.read_csv('silicon_valley_news.csv')
crypto_market_analysis_results = pd.read_csv('crypto_market_analysis_results.txt')

# Clean the input files
silicon_valley_news = silicon_valley_news.dropna()
silicon_valley_news = silicon_valley_news.reset_index(drop=True)
silicon_valley_news = silicon_valley_news.drop_duplicates()
silicon_valley_news = silicon_valley_news.rename(columns={'id': 'index', 'title': 'title', 'content': 'content', 'date': 'date', 'source': 'source', 'url': 'url'})
silicon_valley_news = silicon_valley_news[silicon_valley_news['title'].str.contains('Silicon Valley')]

crypto_market_analysis_results = pd.read_csv('crypto_market_analysis_results.txt')
crypto_market_analysis_results = crypto_market_analysis_results.dropna()
crypto_market_analysis_results = crypto_market_analysis_results.reset_index(drop=True)
crypto_market_analysis_results = crypto_market_analysis_results.drop_duplicates()
crypto_market_analysis_results = crypto_market_analysis_results.rename(columns={'id': 'index', 'crypto_name': 'crypto_name', 'market_cap': 'market_cap', 'total_volume': 'total_volume', 'price': 'price', 'change_percentage_24h': 'change_percentage_24h'})

# Merge the two files on the date column
merged_data = pd.merge(silicon_valley_news, crypto_market_analysis_results, on='date')

# Clean the merged data
merged_data = merged_data.dropna()
merged_data = merged_data.reset_index(drop=True)
merged_data = merged_data.drop_duplicates()
merged_data = merged_data.rename(columns={'index': 'index', 'title': 'title', 'content': 'content', 'date': 'date', 'source': 'source', 'url': 'url', 'crypto_name': 'crypto_name', 'market_cap': 'market_cap', 'total_volume': 'total_volume', 'price': 'price', 'change_percentage_24h': 'change_percentage_24h'})

# Filter the data to keep only the entries where the Silicon Valley news contains the word "crypto"
merged_data = merged_data[merged_data['title'].str.contains('crypto')]

# Calculate the correlation between the change percentage of the crypto and the Silicon Valley news sentiment
correlation = merged_data['change_percentage_24h'].corr(merged_data['title'].apply(lambda x: re.search(r'positive|negative|neutral', x).group()))

# If the correlation is positive, recommend to invest in the crypto
if correlation > 0:
    investment_results = merged_data[merged_data['crypto_name'].isin(['Bitcoin', 'Ethereum', 'Ripple'])]
    investment_results = investment_results.dropna()
    investment_results = investment_results.reset_index(drop=True)
    investment_results = investment_results.drop_duplicates()
    investment_results = investment_results.rename(columns={'index': 'index', 'crypto_name': 'crypto_name', 'market_cap': 'market_cap', 'total_volume': 'total_volume', 'price': 'price', 'change_percentage_24h': 'change_percentage_24h'})
    investment_results.to_csv('investment_results.txt', index=False)

# If the correlation is negative, recommend to sell the crypto
elif correlation < 0:
    investment_results = merged_data[merged_data['crypto_name'].isin(['Bitcoin', 'Ethereum', 'Ripple'])]
    investment_results = investment_results.dropna()
    investment_results = investment_results.reset_index(drop=True)
    investment_results = investment_results.drop_duplicates()
    investment_results = investment_results.rename(columns={'index': 'index', 'crypto_name': 'crypto_name', 'market_cap': 'market_cap', 'total_volume': 'total_volume', 'price': 'price', 'change_percentage_24h': 'change_percentage_24h'})
    investment_results['recommendation'] = 'Sell'
    investment_results.to_csv('investment_results.txt', index=False)

# If the correlation is 0, recommend to hold the crypto
else:
    investment_results = merged_data[merged_data['crypto_name'].isin(['Bitcoin', 'Ethereum', 'Ripple'])]
    investment_results = investment_results.dropna()
    investment_results = investment_results.reset_index(drop=True)
    investment_results = investment_results.drop_duplicates()
    investment_results = investment_results.rename(columns={'index': 'index', 'crypto_name': 'crypto_name', 'market_cap': 'market_cap', 'total_volume': 'total_volume', 'price': 'price', 'change_percentage_24h': 'change_percentage_24h'})
    investment_results['recommendation'] = 'Hold'
    investment_results.to_csv('investment_results.txt', index=False)

