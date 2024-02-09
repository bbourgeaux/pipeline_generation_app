import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
nltk.download('vader_lexicon')
nlp = spacy.load('en_core_web_sm')
# Load the cleaned headlines
headlines = pd.read_csv('clean_headlines.ext')
# Perform sentiment analysis on the headlines
sia = SentimentIntensityAnalyzer()
for i in range(len(headlines)):
    headlines['sentiment'] = sia.polarity_scores(headlines['headlines'][i]['text'])
# Save the sentiment analysis results
headlines.to_csv('sentiment_analysis.ext', index=False)
