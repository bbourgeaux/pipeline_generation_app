import pandas as pd

# Load the crypto_trends.ext file
crypto_trends = pd.read_csv('crypto_trends.ext')

# Perform investment analysis on the crypto_trends.ext file
analysis = crypto_trends.groupby('Trend')['Price'].agg(['min', 'max', 'mean'])

# Save the investment analysis results to investment_analysis.ext file
analysis.to_csv('investment_analysis.ext')

