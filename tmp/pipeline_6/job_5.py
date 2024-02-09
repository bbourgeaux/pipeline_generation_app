
import pandas as pd

# Read the input file
crypto_market_analysis_results = pd.read_csv('crypto_market_analysis_results.txt')

# Perform investment recommendation
investment_recommendation_results = crypto_market_analysis_results.groupby('crypto')['price_change_percentage_24h'].max()

# Write the output file
investment_recommendation_results.to_csv('investment_recommendation_results.txt')

